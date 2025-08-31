from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import UserSubmission
from forms import InterestForm, AdminSearchForm
from email_service import send_bulk_emails
import logging

@app.route('/')
def index():
    """Homepage with AstraZeneca branding and clinical trial information"""
    return render_template('index.html')

@app.route('/interest', methods=['GET', 'POST'])
def interest_form():
    """Interest form for clinical trial registration"""
    form = InterestForm()
    
    if form.validate_on_submit():
        # Create new user submission
        submission = UserSubmission(
            name=form.name.data,
            email=form.email.data,
            mobile=form.mobile.data,
            pincode=form.pincode.data,
            age=form.age.data,
            health_info=form.health_info.data,
            is_eligible=UserSubmission.check_eligibility(form.age.data, form.pincode.data)
        )
        
        try:
            db.session.add(submission)
            db.session.commit()
            
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

@app.route('/admin')
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

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
