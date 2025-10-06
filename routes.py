from flask import render_template, request, redirect, url_for, flash, jsonify, session
from app import app, db
from models import UserSubmission, check_clinical_trial_eligibility, get_eligibility_message, check_cell_therapy_eligibility
from forms import InterestForm, AdminSearchForm, AdminLoginForm, CellTherapyInterestForm
from email_service import send_bulk_emails
from clinical_trials_scraper import scraper
import logging
import os
import json
from functools import wraps

@app.route('/')
def index():
    """Homepage with AstraZeneca branding and clinical trial information"""
    return render_template('index.html')

@app.route('/interest', methods=['GET', 'POST'])
def interest_form():
    """Interest form for clinical trial registration"""
    form = InterestForm()
    
    if form.validate_on_submit():
        # Perform comprehensive eligibility check
        is_eligible, reasons = check_clinical_trial_eligibility(
            age=form.age.data,
            zipcode=form.zipcode.data,
            health_info=form.health_info.data,
            mobile=form.mobile.data
        )
        
        # Generate user-friendly message
        message_type, message = get_eligibility_message(is_eligible, reasons)
        
        # Create new user submission
        submission = UserSubmission(
            name=form.name.data,
            email=form.email.data,
            mobile=form.mobile.data,
            pincode=form.zipcode.data,
            age=form.age.data,
            health_info=form.health_info.data,
            is_eligible=is_eligible
        )
        
        try:
            db.session.add(submission)
            db.session.commit()
            
            # Flash appropriate message based on eligibility
            flash(message, message_type)
            
            # Always redirect to confirmation page
            return redirect(url_for('confirmation', submission_id=submission.id))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting your form. Please try again.', 'error')
            logging.error(f"Error saving submission: {e}")
    
    return render_template('form.html', form=form)

@app.route('/confirmation/<int:submission_id>')
def confirmation(submission_id):
    """Confirmation page after successful submission"""
    submission = UserSubmission.query.get_or_404(submission_id)
    return render_template('confirmation.html', submission=submission)

@app.route('/celltherapy')
def celltherapy():
    """Clinical Trials landing page with trial information"""
    # Fetch real-time status for featured trials
    locus_data = scraper.fetch_trial_details('NCT06194461')
    athena_data = scraper.fetch_trial_details('NCT06084884')
    
    # Static trials (keep as primary featured trials)
    static_trials = {
        'locus': {
            'name': 'LOCUS - Long-term Follow-up Study',
            'nct_id': 'NCT06194461',
            'description': 'Master long-term follow-up protocol for participants who received cell or gene therapies in other AstraZeneca studies',
            'phase': 'Phase 1/2',
            'condition': 'Hepatocellular Carcinoma',
            'age_range': '13 years minimum',
            'status': locus_data.get('overall_status', 'NOT_YET_RECRUITING') if locus_data else 'NOT_YET_RECRUITING',
            'duration': 'Up to 15 years post-treatment monitoring',
            'is_featured': True,
            'source': 'static'
        },
        'azd5851': {
            'name': 'ATHENA - AZD5851 CAR-T Study',
            'nct_id': 'NCT06084884',
            'description': 'Phase I/II study evaluating AZD5851 CAR-T therapy for GPC3+ advanced/recurrent hepatocellular carcinoma',
            'phase': 'Phase I/II',
            'condition': 'Advanced Hepatocellular Carcinoma',
            'age_range': '18+ years',
            'status': athena_data.get('overall_status', 'RECRUITING') if athena_data else 'RECRUITING',
            'target_enrollment': '94 participants',
            'is_featured': True,
            'source': 'static'
        }
    }
    
    # Get search and filter parameters
    search_query = request.args.get('search', '').strip()
    status_filter = request.args.get('status', '')
    phase_filter = request.args.get('phase', '')
    condition_filter = request.args.get('condition', '')
    page = int(request.args.get('page', 1))
    per_page = 12  # Show 12 trials per page

    # Fetch live API data
    try:
        logging.info("Fetching AstraZeneca cell therapy trials from API...")
        api_trials = scraper.fetch_astrazeneca_cell_therapy_trials(page_size=500)
        logging.info(f"Fetched {len(api_trials)} trials from API")
        
        # Collect unique status values for filtering
        all_statuses = set()
        all_phases = set()
        
        # Process and filter API trials
        processed_api_trials = []
        for trial in api_trials:
            # Skip if this is one of our static trials
            if trial.get('nct_id') not in ['NCT06194461', 'NCT06084884']:
                # Extract locations properly
                locations = trial.get('locations', [])
                valid_locations = [loc for loc in locations if loc.get('facility_name')]
                
                # Ensure this is an AstraZeneca trial
                sponsor_name = trial.get('lead_sponsor', '')
                if 'astrazeneca' not in sponsor_name.lower():
                    continue
                
                processed_trial = {
                    'name': trial.get('brief_title', 'Unknown Trial'),
                    'nct_id': trial.get('nct_id'),
                    'description': trial.get('brief_summary', trial.get('detailed_description', 'No description available'))[:200] + '...' if trial.get('brief_summary') else 'No description available',
                    'phase': ', '.join(trial.get('phases', [])) if trial.get('phases') else 'Unknown Phase',
                    'condition': ', '.join(trial.get('conditions', [])) if trial.get('conditions') else 'Unknown Condition',
                    'status': trial.get('overall_status', 'Unknown Status'),
                    'sponsor': sponsor_name or 'AstraZeneca',
                    'enrollment': trial.get('enrollment'),
                    'is_featured': False,
                    'source': 'api',
                    'locations_count': len(valid_locations),
                    'locations': valid_locations[:3],  # Show first 3 locations in bento box
                    'total_locations': len(valid_locations),
                    'last_updated': trial.get('last_update_submitted_date')
                }
                
                # Collect unique statuses and phases for filtering
                all_statuses.add(processed_trial['status'])
                if trial.get('phases'):
                    for phase in trial.get('phases', []):
                        all_phases.add(phase)
                
                # Apply filters
                if search_query:
                    if not (search_query.lower() in processed_trial['name'].lower() or 
                           search_query.lower() in processed_trial['description'].lower() or
                           search_query.lower() in processed_trial['condition'].lower()):
                        continue
                
                # Improved status filtering - exact match for better accuracy
                if status_filter and status_filter != processed_trial['status']:
                    continue
                
                # Improved phase filtering - check if any of the trial's phases match
                if phase_filter:
                    trial_phases = trial.get('phases', [])
                    if not any(phase_filter in phase for phase in trial_phases):
                        continue
                    
                if condition_filter and condition_filter.lower() not in processed_trial['condition'].lower():
                    continue
                
                processed_api_trials.append(processed_trial)
        
        # Pagination
        total_trials = len(processed_api_trials)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_trials = processed_api_trials[start_idx:end_idx]
        
        # Calculate pagination info
        total_pages = (total_trials + per_page - 1) // per_page
        has_prev = page > 1
        has_next = page < total_pages
    
    except Exception as e:
        logging.error(f"Error fetching API trials: {str(e)}")
        paginated_trials = []
        total_trials = 0
        total_pages = 0
        has_prev = has_next = False
        flash('Unable to load latest trial data. Showing available trials.', 'warning')
        all_statuses = set()
        all_phases = set()
    
    locations = [
        {'name': 'UCSF (University of California, San Francisco)', 'contact': '888-689-8273'},
        {'name': 'Multiple International Sites', 'contact': 'Contact study coordinator'}
    ]
    
    return render_template('celltherapy.html', 
                         static_trials=static_trials, 
                         api_trials=paginated_trials,
                         locations=locations,
                         total_trials=len(static_trials) + total_trials,
                         current_page=page,
                         total_pages=total_pages,
                         has_prev=has_prev,
                         has_next=has_next,
                         search_query=search_query,
                         status_filter=status_filter,
                         phase_filter=phase_filter,
                         condition_filter=condition_filter,
                         showing_results=len(paginated_trials),
                         filtered_total=total_trials,
                         available_statuses=sorted(all_statuses),
                         available_phases=sorted(all_phases))

@app.route('/trial/<nct_id>')
def trial_details(nct_id):
    """Detailed view of a specific clinical trial"""
    try:
        # Try to get detailed trial information from API
        trial_data = scraper.fetch_trial_details(nct_id)
        
        if not trial_data:
            flash(f'Trial {nct_id} not found or unavailable.', 'error')
            return redirect(url_for('celltherapy'))
        
        # Format trial data for display
        formatted_trial = {
            'basic_info': {
                'nct_id': trial_data.get('nct_id'),
                'brief_title': trial_data.get('brief_title'),
                'official_title': trial_data.get('official_title'),
                'acronym': trial_data.get('acronym'),
                'overall_status': trial_data.get('overall_status'),
                'study_type': trial_data.get('study_type'),
                'phases': trial_data.get('phases', [])
            },
            'dates': {
                'start_date': trial_data.get('start_date'),
                'primary_completion_date': trial_data.get('primary_completion_date'),
                'completion_date': trial_data.get('completion_date'),
                'last_updated': trial_data.get('last_update_submitted_date')
            },
            'sponsor_info': {
                'lead_sponsor': trial_data.get('lead_sponsor'),
                'lead_sponsor_class': trial_data.get('lead_sponsor_class'),
                'collaborators': trial_data.get('collaborators', [])
            },
            'study_design': {
                'allocation': trial_data.get('allocation'),
                'intervention_model': trial_data.get('intervention_model'),
                'primary_purpose': trial_data.get('primary_purpose'),
                'masking': trial_data.get('masking'),
                'enrollment': trial_data.get('enrollment')
            },
            'conditions_interventions': {
                'conditions': trial_data.get('conditions', []),
                'interventions': trial_data.get('interventions', []),
                'keywords': trial_data.get('keywords', [])
            },
            'eligibility': {
                'criteria': trial_data.get('eligibility_criteria'),
                'healthy_volunteers': trial_data.get('healthy_volunteers'),
                'gender': trial_data.get('gender'),
                'minimum_age': trial_data.get('minimum_age'),
                'maximum_age': trial_data.get('maximum_age')
            },
            'descriptions': {
                'brief_summary': trial_data.get('brief_summary'),
                'detailed_description': trial_data.get('detailed_description')
            },
            'locations': trial_data.get('locations', []),
            'contacts': trial_data.get('central_contacts', []),
            'raw_data': trial_data.get('raw_data', {})
        }
        
        return render_template('trial_details.html', trial=formatted_trial)
        
    except Exception as e:
        logging.error(f"Error fetching trial details for {nct_id}: {str(e)}")
        flash(f'Error loading trial details for {nct_id}. Please try again.', 'error')
        return redirect(url_for('celltherapy'))

@app.route('/celltherapy/interest', methods=['GET', 'POST'])
@app.route('/celltherapy/interest/<nct_id>', methods=['GET', 'POST'])
def celltherapy_interest(nct_id=None):
    """Cell therapy specific interest form - can be trial-specific"""
    form = CellTherapyInterestForm()
    trial_info = None
    
    # If NCT ID is provided, get trial information
    if nct_id:
        try:
            trial_info = scraper.fetch_trial_details(nct_id)
            if not trial_info:
                flash(f'Trial {nct_id} not found. Showing general interest form.', 'warning')
                nct_id = None
        except Exception as e:
            logging.error(f"Error fetching trial info for {nct_id}: {e}")
            flash('Unable to load specific trial information. Showing general form.', 'warning')
            nct_id = None
    
    if form.validate_on_submit():
        # Cell therapy specific eligibility check
        is_eligible, reasons = check_cell_therapy_eligibility(
            age=form.age.data,
            zipcode=form.zipcode.data,
            diagnosis=form.diagnosis.data,
            health_status=form.current_health_status.data
        )
        
        # Generate user-friendly message for cell therapy
        message_type, message = get_eligibility_message(is_eligible, reasons)
        
        # Create new cell therapy submission
        submission = UserSubmission(
            name=form.name.data,
            email=form.email.data,
            mobile=form.mobile.data,
            pincode=form.zipcode.data,
            age=form.age.data,
            health_info=form.current_health_status.data,
            is_eligible=is_eligible,
            therapy_type='cell_therapy',
            diagnosis=form.diagnosis.data,
            current_health_status=form.current_health_status.data,
            specific_trial_nct=nct_id  # Store specific trial interest
        )
        
        try:
            db.session.add(submission)
            db.session.commit()
            
            flash(message, message_type)
            
            return redirect(url_for('celltherapy_confirmation', submission_id=submission.id))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting your form. Please try again.', 'error')
            logging.error(f"Error saving cell therapy submission: {e}")
    
    return render_template('celltherapy_form.html', form=form, trial_info=trial_info, nct_id=nct_id)

@app.route('/celltherapy/confirmation/<int:submission_id>')
def celltherapy_confirmation(submission_id):
    """Confirmation page for cell therapy submission"""
    submission = UserSubmission.query.get_or_404(submission_id)
    if submission.therapy_type != 'cell_therapy':
        flash('Invalid submission type', 'error')
        return redirect(url_for('celltherapy'))
    
    return render_template('celltherapy_confirmation.html', submission=submission)

def admin_required(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    form = AdminLoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Check credentials against environment variables
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        
        if username == admin_username and password == admin_password:
            session['admin_logged_in'] = True
            flash('Successfully logged in to admin panel', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin_login.html', form=form)

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard for managing submissions"""
    search_form = AdminSearchForm()
    
    # Get all submissions
    query = UserSubmission.query
    
    # Apply filters if provided
    zipcode_filter = request.args.get('search_zipcode', '').strip()
    eligibility_filter = request.args.get('eligibility_filter', '')
    therapy_filter = request.args.get('therapy_filter', '')
    
    if zipcode_filter:
        query = query.filter(UserSubmission.pincode.contains(zipcode_filter))
    
    if eligibility_filter == 'eligible':
        query = query.filter(UserSubmission.is_eligible == True)
    elif eligibility_filter == 'not_eligible':
        query = query.filter(UserSubmission.is_eligible == False)
    
    if therapy_filter == 'general':
        query = query.filter(UserSubmission.therapy_type == 'general')
    elif therapy_filter == 'cell_therapy':
        query = query.filter(UserSubmission.therapy_type == 'cell_therapy')
    
    submissions = query.order_by(UserSubmission.created_at.desc()).all()
    
    # Statistics
    total_submissions = UserSubmission.query.count()
    eligible_count = UserSubmission.query.filter(UserSubmission.is_eligible == True).count()
    emails_sent_count = UserSubmission.query.filter(UserSubmission.email_sent == True).count()
    cell_therapy_count = UserSubmission.query.filter(UserSubmission.therapy_type == 'cell_therapy').count()
    general_count = UserSubmission.query.filter(UserSubmission.therapy_type == 'general').count()
    
    stats = {
        'total': total_submissions,
        'eligible': eligible_count,
        'not_eligible': total_submissions - eligible_count,
        'emails_sent': emails_sent_count,
        'cell_therapy': cell_therapy_count,
        'general': general_count
    }
    
    return render_template('admin/dashboard.html', 
                         submissions=submissions, 
                         search_form=search_form,
                         stats=stats,
                         current_zipcode=zipcode_filter,
                         current_eligibility=eligibility_filter,
                         current_therapy=therapy_filter)

@app.route('/admin/send_emails', methods=['POST'])
@admin_required
def send_emails():
    """Send bulk emails to selected submissions"""
    selected_ids = request.form.getlist('selected_submissions')
    
    if not selected_ids:
        flash('Please select at least one submission to send emails.', 'warning')
        return redirect(url_for('admin_dashboard'))
    
    try:
        # Get selected submissions
        selected_submissions = UserSubmission.query.filter(
            UserSubmission.id.in_(selected_ids)
        ).all()
        
        # Send emails
        success_count, error_count, success_emails = send_bulk_emails(selected_submissions)
        
        # Update database for successful emails
        if success_emails:
            for submission in selected_submissions:
                if submission.email in success_emails:
                    submission.email_sent = True
            db.session.commit()
        
        if success_count > 0:
            flash(f'Successfully sent {success_count} emails.', 'success')
        
        if error_count > 0:
            flash(f'Failed to send {error_count} emails. Please check your email configuration.', 'error')
            
    except Exception as e:
        flash(f'An error occurred while sending emails: {str(e)}', 'error')
        logging.error(f"Error sending bulk emails: {e}")
    
    return redirect(url_for('admin_dashboard'))

@app.route('/api/check_eligibility', methods=['POST'])
def api_check_eligibility():
    """
    API endpoint for real-time eligibility checking
    
    Expected JSON payload:
    {
        "age": 25,
        "zipcode": "90210",
        "health_info": "No major health issues",
        "mobile": "9876543210"
    }
    
    Returns:
    {
        "is_eligible": true/false,
        "reasons": ["list of issues"],
        "message": "user-friendly message",
        "message_type": "success/warning/error"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Invalid JSON data',
                'is_eligible': False
            }), 400
        
        # Validate required fields
        required_fields = ['age', 'zipcode', 'health_info']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'is_eligible': False
            }), 400
        
        # Perform eligibility check
        is_eligible, reasons = check_clinical_trial_eligibility(
            age=data['age'],
            zipcode=data['zipcode'],
            health_info=data['health_info'],
            mobile=data.get('mobile'),
            additional_checks=data.get('additional_checks')
        )
        
        # Generate user-friendly message
        message_type, message = get_eligibility_message(is_eligible, reasons)
        
        return jsonify({
            'is_eligible': is_eligible,
            'reasons': reasons,
            'message': message,
            'message_type': message_type
        })
        
    except Exception as e:
        logging.error(f"Error in eligibility check API: {e}")
        return jsonify({
            'error': 'Internal server error',
            'is_eligible': False
        }), 500

# Individual Clinical Trial Pages
@app.route('/trial/locus')
def trial_locus():
    """LOCUS Trial Detail Page - NCT06194461"""
    return render_template('trial_locus.html')

@app.route('/trial/azd5851')
def trial_azd5851():
    """AZD5851 Trial Detail Page - NCT06084884"""
    return render_template('trial_azd5851.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
