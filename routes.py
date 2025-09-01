from flask import render_template, request, redirect, url_for, flash, jsonify, session
from app import app, db
from models import UserSubmission, check_clinical_trial_eligibility, get_eligibility_message
from forms import InterestForm, AdminSearchForm, AdminLoginForm
from email_service import send_bulk_emails
import logging
import os
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
            pincode=form.pincode.data,
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
            pincode=form.pincode.data,
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
    pincode_filter = request.args.get('search_pincode', '').strip()
    eligibility_filter = request.args.get('eligibility_filter', '')
    
    if pincode_filter:
        query = query.filter(UserSubmission.pincode.contains(pincode_filter))
    
    if eligibility_filter == 'eligible':
        query = query.filter(UserSubmission.is_eligible == True)
    elif eligibility_filter == 'not_eligible':
        query = query.filter(UserSubmission.is_eligible == False)
    
    submissions = query.order_by(UserSubmission.created_at.desc()).all()
    
    # Statistics
    total_submissions = UserSubmission.query.count()
    eligible_count = UserSubmission.query.filter(UserSubmission.is_eligible == True).count()
    emails_sent_count = UserSubmission.query.filter(UserSubmission.email_sent == True).count()
    
    stats = {
        'total': total_submissions,
        'eligible': eligible_count,
        'not_eligible': total_submissions - eligible_count,
        'emails_sent': emails_sent_count
    }
    
    return render_template('admin/dashboard.html', 
                         submissions=submissions, 
                         search_form=search_form,
                         stats=stats,
                         current_pincode=pincode_filter,
                         current_eligibility=eligibility_filter)

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
        success_count, error_count = send_bulk_emails(selected_submissions)
        
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
        "pincode": "560001",
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
        required_fields = ['age', 'pincode', 'health_info']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'is_eligible': False
            }), 400
        
        # Perform eligibility check
        is_eligible, reasons = check_clinical_trial_eligibility(
            age=data['age'],
            pincode=data['pincode'],
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

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
