"""
AstraZeneca Clinical Trials - Email Service Usage Examples

This module demonstrates how to use the enhanced email service
for sending personalized emails via SMTP.
"""

# Example 1: Simple single email
def example_send_single_email():
    """Send a welcome email to one recipient"""
    from email_service import send_welcome_email
    
    result = send_welcome_email(
        recipient_email='user@example.com',
        recipient_name='John Doe',
        pincode='110001'
    )
    
    if result['status'] == 'success':
        print('Welcome email sent successfully!')
    else:
        print(f'Failed to send email: {result["message"]}')
    
    return result

# Example 2: Bulk custom emails
def example_send_bulk_emails():
    """Send custom emails to multiple recipients"""
    from email_service import send_custom_email
    
    recipients = [
        {'email': 'john@example.com', 'name': 'John', 'pincode': '110001'},
        {'email': 'jane@example.com', 'name': 'Jane', 'pincode': '400001'}
    ]
    
    subject = "Clinical Trial Update - {name}"
    template = """
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #8A0051;">Dear {name},</h2>
        <p>AstraZeneca has clinical trials in your area {pincode}. Learn more and participate!</p>
        <p>We have identified trials in {locality} that match your profile.</p>
        <p>Best regards,<br>AstraZeneca Clinical Research Team</p>
    </body>
    </html>
    """
    
    result = send_custom_email(recipients, subject, template)
    print(f"Sent {result['success_count']} emails successfully")
    
    return result

# Example 3: Using EmailService directly
def example_email_service_direct():
    """Use EmailService class directly for advanced features"""
    from email_service import email_service
    
    recipients = [
        {
            'email': 'participant@example.com',
            'name': 'Alice Cooper',
            'pincode': '110001',
            'age': 45
        }
    ]
    
    subject = "Personalized Clinical Trial - {name}"
    template = """
    <html>
    <body>
        <h2>Dear {name},</h2>
        <p>Based on your age ({age}), we have trials in {locality} for you.</p>
        <p>Contact us to learn more!</p>
    </body>
    </html>
    """
    
    result = email_service.send_personalized_emails(
        recipients=recipients,
        subject=subject,
        template=template
    )
    
    return result

# Example 4: Flask route integration
def example_flask_route():
    """Example of email integration in Flask route"""
    # This would be in your routes.py file:
    
    # from flask import request, flash, redirect, url_for
    # from email_service import send_welcome_email
    # from models import UserSubmission
    # from app import db
    
    route_code = '''
    @app.route('/register', methods=['POST'])
    def register_participant():
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email') 
        pincode = request.form.get('pincode')
        
        # Save to database
        submission = UserSubmission(
            name=name,
            email=email,
            pincode=pincode
            # ... other fields
        )
        
        try:
            db.session.add(submission)
            db.session.commit()
            
            # Send welcome email
            email_result = send_welcome_email(email, name, pincode)
            
            if email_result['status'] == 'success':
                submission.email_sent = True
                db.session.commit()
                flash('Registration successful! Welcome email sent.', 'success')
            else:
                flash('Registration successful! Email will be sent later.', 'info')
            
            return redirect(url_for('confirmation'))
            
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
    '''
    
    return route_code

# Example 5: Admin bulk email function
def example_admin_bulk():
    """Example admin function for bulk emails"""
    admin_code = '''
    @app.route('/admin/send_emails', methods=['POST'])
    def admin_send_bulk_emails():
        from email_service import send_bulk_emails
        from models import UserSubmission
        
        # Get selected submission IDs
        selected_ids = request.form.getlist('selected_submissions')
        
        # Get submissions from database
        submissions = UserSubmission.query.filter(
            UserSubmission.id.in_(selected_ids)
        ).all()
        
        # Send bulk emails
        success_count, error_count = send_bulk_emails(submissions)
        
        # Flash results
        if success_count > 0:
            flash(f'Successfully sent {success_count} emails', 'success')
        if error_count > 0:
            flash(f'Failed to send {error_count} emails', 'error')
        
        return redirect(url_for('admin_dashboard'))
    '''
    
    return admin_code

# Environment setup instructions
def get_environment_setup():
    """Instructions for setting up environment variables"""
    return """
    Required Environment Variables for Gmail SMTP:
    
    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=587
    SMTP_USERNAME=your-email@gmail.com
    SMTP_PASSWORD=your-app-password
    FROM_EMAIL=your-email@gmail.com (optional)
    
    Gmail Setup:
    1. Enable 2-factor authentication on your Gmail account
    2. Generate an app password for this application
    3. Use the app password, not your regular Gmail password
    4. Set the environment variables in your Replit secrets
    """

# Template placeholder reference
def get_template_placeholders():
    """Available template placeholders"""
    return """
    Available Template Placeholders:
    
    {name}      - Recipient's full name
    {email}     - Recipient's email address
    {pincode}   - Recipient's postal code
    {locality}  - City/region based on pincode
    {age}       - Recipient's age (if provided)
    
    Custom placeholders can be added by including them
    in the recipients data dictionary.
    
    Example:
    recipients = [
        {
            'email': 'user@example.com',
            'name': 'John Doe',
            'pincode': '110001',
            'custom_field': 'Custom Value'
        }
    ]
    
    Template: "Hello {name}, your custom data: {custom_field}"
    """

if __name__ == "__main__":
    print("Email Service Examples")
    print("=" * 50)
    
    print("\n1. Environment Setup:")
    print(get_environment_setup())
    
    print("\n2. Template Placeholders:")
    print(get_template_placeholders())
    
    print("\n3. Test single email (requires SMTP setup):")
    # Uncomment to test:
    # example_send_single_email()