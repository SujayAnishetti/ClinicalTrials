import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Tuple, Optional
from app import db

class EmailService:
    """
    SMTP Email Service for AstraZeneca Clinical Trials
    
    Handles sending personalized emails via Gmail SMTP with TLS encryption.
    Supports template-based emails with placeholder substitution.
    """
    
    def __init__(self):
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        self.smtp_username = os.environ.get('SMTP_USERNAME', '')
        self.smtp_password = os.environ.get('SMTP_PASSWORD', '')
        self.from_email = os.environ.get('FROM_EMAIL', self.smtp_username)
        
        # Validate required credentials
        if not self.smtp_username or not self.smtp_password:
            logging.warning("SMTP credentials not configured. Email functionality will be limited.")
    
    def send_personalized_emails(self, recipients: List[Dict], subject: str, 
                               template: str, template_vars: Optional[Dict] = None) -> Dict:
        """
        Send personalized emails to multiple recipients
        
        Args:
            recipients: List of dicts with 'email', 'name', and other personal data
            subject: Email subject line
            template: Email template with placeholders like {name}, {pincode}
            template_vars: Global template variables applied to all emails
            
        Returns:
            Dict with success_count, error_count, and detailed results per recipient
        """
        if not self.smtp_username or not self.smtp_password:
            return {
                'success_count': 0,
                'error_count': len(recipients),
                'results': [{'email': r['email'], 'status': 'error', 'message': 'SMTP credentials not configured'} for r in recipients]
            }
        
        results = []
        success_count = 0
        error_count = 0
        
        try:
            # Create SMTP session
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable TLS encryption
            server.login(self.smtp_username, self.smtp_password)
            
            for recipient in recipients:
                try:
                    # Prepare personalized template variables
                    personal_vars = template_vars.copy() if template_vars else {}
                    personal_vars.update(recipient)
                    
                    # Generate personalized content
                    personalized_subject = subject.format(**personal_vars)
                    personalized_body = template.format(**personal_vars)
                    
                    # Create email message
                    msg = MIMEMultipart('alternative')
                    msg['From'] = self.from_email
                    msg['To'] = recipient['email']
                    msg['Subject'] = personalized_subject
                    
                    # Add HTML content
                    html_part = MIMEText(personalized_body, 'html')
                    msg.attach(html_part)
                    
                    # Send email
                    server.send_message(msg)
                    
                    # Record success
                    results.append({
                        'email': recipient['email'],
                        'status': 'success',
                        'message': 'Email sent successfully'
                    })
                    success_count += 1
                    
                    logging.info(f"Email sent successfully to {recipient['email']}")
                    
                except KeyError as e:
                    error_msg = f"Missing template variable: {str(e)}"
                    results.append({
                        'email': recipient['email'],
                        'status': 'error',
                        'message': error_msg
                    })
                    error_count += 1
                    logging.error(f"Template error for {recipient['email']}: {error_msg}")
                    
                except Exception as e:
                    error_msg = f"Failed to send email: {str(e)}"
                    results.append({
                        'email': recipient['email'],
                        'status': 'error',
                        'message': error_msg
                    })
                    error_count += 1
                    logging.error(f"Failed to send email to {recipient['email']}: {error_msg}")
            
            # Close SMTP session
            server.quit()
            
        except Exception as e:
            error_msg = f"SMTP connection error: {str(e)}"
            logging.error(error_msg)
            
            # Mark all as failed if connection failed
            for recipient in recipients:
                if not any(r['email'] == recipient['email'] for r in results):
                    results.append({
                        'email': recipient['email'],
                        'status': 'error',
                        'message': error_msg
                    })
                    error_count += 1
        
        return {
            'success_count': success_count,
            'error_count': error_count,
            'results': results
        }
    
    def send_single_email(self, recipient_email: str, subject: str, 
                         body: str, is_html: bool = True) -> Dict:
        """
        Send a single email
        
        Args:
            recipient_email: Recipient's email address
            subject: Email subject
            body: Email body content
            is_html: Whether body contains HTML content
            
        Returns:
            Dict with status and message
        """
        recipients = [{'email': recipient_email, 'name': ''}]
        template = body
        
        result = self.send_personalized_emails(recipients, subject, template)
        
        if result['results']:
            return result['results'][0]
        else:
            return {'status': 'error', 'message': 'Unknown error occurred'}

# Create global email service instance
email_service = EmailService()

def get_email_template(user_name, pincode):
    """Generate email template with user-specific content"""
    
    # Map pincodes to regions for localized content
    region_mapping = {
        '110': 'New Delhi',
        '400': 'Mumbai',
        '560': 'Bangalore',
        '600': 'Chennai',
        '700': 'Kolkata',
        '500': 'Hyderabad',
        '380': 'Ahmedabad',
        '201': 'Ghaziabad',
        '411': 'Pune',
        '302': 'Jaipur'
    }
    
    # Get region based on first 3 digits of pincode
    region = region_mapping.get(pincode[:3], 'your area')
    
    subject = "AstraZeneca Clinical Trials - Thank You for Your Interest"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background-color: #8A0051; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .highlight {{ color: #8A0051; font-weight: bold; }}
            .footer {{ background-color: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; }}
            .button {{ background-color: #EFAB00; color: #8A0051; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>AstraZeneca Clinical Trials</h1>
        </div>
        
        <div class="content">
            <h2>Dear {user_name},</h2>
            
            <p>Thank you for your interest in participating in AstraZeneca clinical trials. We have received your registration and are reviewing your information.</p>
            
            <p>Based on your location in <span class="highlight">{region}</span>, we have identified several clinical trials that may be relevant to you:</p>
            
            <ul>
                <li><strong>Cardiovascular Health Study</strong> - Phase III trial for heart disease prevention</li>
                <li><strong>Respiratory Research Program</strong> - New treatments for asthma and COPD</li>
                <li><strong>Oncology Innovation Trial</strong> - Advanced cancer treatment research</li>
                <li><strong>Diabetes Management Study</strong> - Next-generation diabetes medications</li>
            </ul>
            
            <p>Our clinical research team will contact you within the next 5-7 business days to discuss potential opportunities that match your health profile.</p>
            
            <a href="https://astrazenecaclinicaltrials.com" class="button">Learn More About Our Trials</a>
            
            <h3>What's Next?</h3>
            <ol>
                <li>Our team will review your health information</li>
                <li>We'll match you with suitable clinical trials in {region}</li>
                <li>You'll receive a call to discuss participation options</li>
                <li>If interested, we'll schedule a screening appointment</li>
            </ol>
            
            <p>For more information about clinical trials, visit <a href="https://clinicaltrials.gov">clinicaltrials.gov</a> or our dedicated portal at <a href="https://astrazenecaclinicaltrials.com">astrazenecaclinicaltrials.com</a>.</p>
            
            <p>If you have any questions, please contact our Clinical Trials Information Center at <strong>1-800-TRIALS-1</strong>.</p>
            
            <p>Best regards,<br>
            <span class="highlight">AstraZeneca Clinical Research Team</span></p>
        </div>
        
        <div class="footer">
            <p>AstraZeneca Pharmaceuticals LP | This email is for informational purposes only</p>
            <p>For medical emergencies, please contact your healthcare provider immediately</p>
        </div>
    </body>
    </html>
    """
    
    return subject, html_body

def get_clinical_trial_template():
    """
    Get the clinical trial email template with placeholders
    
    Returns:
        Tuple of (subject_template, body_template)
    """
    subject = "AstraZeneca Clinical Trials - Thank You for Your Interest, {name}"
    
    body = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background-color: #8A0051; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .highlight {{ color: #8A0051; font-weight: bold; }}
            .footer {{ background-color: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; }}
            .button {{ background-color: #EFAB00; color: #8A0051; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>AstraZeneca Clinical Trials</h1>
        </div>
        
        <div class="content">
            <h2>Dear {name},</h2>
            
            <p>Thank you for your interest in participating in AstraZeneca clinical trials. We have received your registration and are reviewing your information.</p>
            
            <p>Based on your location in <span class="highlight">{locality}</span> (Pincode: {pincode}), we have identified several clinical trials that may be relevant to you:</p>
            
            <ul>
                <li><strong>Cardiovascular Health Study</strong> - Phase III trial for heart disease prevention</li>
                <li><strong>Respiratory Research Program</strong> - New treatments for asthma and COPD</li>
                <li><strong>Oncology Innovation Trial</strong> - Advanced cancer treatment research</li>
                <li><strong>Diabetes Management Study</strong> - Next-generation diabetes medications</li>
            </ul>
            
            <p>Our clinical research team will contact you within the next 5-7 business days to discuss potential opportunities that match your health profile.</p>
            
            <a href="https://astrazenecaclinicaltrials.com" class="button">Learn More About Our Trials</a>
            
            <h3>What's Next?</h3>
            <ol>
                <li>Our team will review your health information</li>
                <li>We'll match you with suitable clinical trials in {locality}</li>
                <li>You'll receive a call to discuss participation options</li>
                <li>If interested, we'll schedule a screening appointment</li>
            </ol>
            
            <p>For more information about clinical trials, visit <a href="https://clinicaltrials.gov">clinicaltrials.gov</a> or our dedicated portal at <a href="https://astrazenecaclinicaltrials.com">astrazenecaclinicaltrials.com</a>.</p>
            
            <p>If you have any questions, please contact our Clinical Trials Information Center at <strong>1-800-TRIALS-1</strong>.</p>
            
            <p>Best regards,<br>
            <span class="highlight">AstraZeneca Clinical Research Team</span></p>
        </div>
        
        <div class="footer">
            <p>AstraZeneca Pharmaceuticals LP | This email is for informational purposes only</p>
            <p>For medical emergencies, please contact your healthcare provider immediately</p>
        </div>
    </body>
    </html>
    """
    
    return subject, body

def get_simple_template():
    """
    Get a simple email template as requested in the example
    
    Returns:
        Tuple of (subject_template, body_template)
    """
    subject = "AstraZeneca Clinical Trials in Your Area - {name}"
    
    body = """
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2 style="color: #8A0051;">Dear {name},</h2>
        
        <p>AstraZeneca has clinical trials in your area {pincode}. Learn more and participate!</p>
        
        <p>We believe you might be interested in our ongoing clinical research studies in {locality}.</p>
        
        <p>Visit our portal to learn more: <a href="https://astrazenecaclinicaltrials.com">AstraZeneca Clinical Trials</a></p>
        
        <p>Best regards,<br>
        AstraZeneca Clinical Research Team</p>
    </body>
    </html>
    """
    
    return subject, body

def send_bulk_emails(submissions):
    """
    Send emails to multiple submissions using the new EmailService
    
    Args:
        submissions: List of UserSubmission objects from database
        
    Returns:
        Tuple of (success_count, error_count)
    """
    
    # Prepare recipients data
    recipients = []
    for submission in submissions:
        # Map pincode to locality
        locality = get_locality_from_pincode(submission.pincode)
        
        recipients.append({
            'email': submission.email,
            'name': submission.name,
            'pincode': submission.pincode,
            'locality': locality,
            'age': submission.age
        })
    
    # Get email template
    subject_template, body_template = get_clinical_trial_template()
    
    # Send emails using the new service
    result = email_service.send_personalized_emails(
        recipients=recipients,
        subject=subject_template,
        template=body_template
    )
    
    # Update database for successful sends
    success_emails = [r['email'] for r in result['results'] if r['status'] == 'success']
    
    if success_emails:
        for submission in submissions:
            if submission.email in success_emails:
                submission.email_sent = True
        
        try:
            db.session.commit()
        except Exception as e:
            logging.error(f"Failed to update database: {e}")
    
    return result['success_count'], result['error_count']

def get_locality_from_pincode(pincode):
    """Map pincode to locality name"""
    region_mapping = {
        '110': 'New Delhi',
        '400': 'Mumbai', 
        '560': 'Bangalore',
        '600': 'Chennai',
        '700': 'Kolkata',
        '500': 'Hyderabad',
        '380': 'Ahmedabad',
        '201': 'Ghaziabad',
        '411': 'Pune',
        '302': 'Jaipur'
    }
    
    return region_mapping.get(pincode[:3], 'your area')

# Example usage functions for Flask routes
def send_welcome_email(recipient_email: str, recipient_name: str, pincode: str) -> Dict:
    """
    Send a welcome email to a single recipient
    
    Example usage in Flask route:
        result = send_welcome_email('user@example.com', 'John Doe', '110001')
        if result['status'] == 'success':
            flash('Welcome email sent successfully!', 'success')
        else:
            flash(f'Failed to send email: {result["message"]}', 'error')
    """
    locality = get_locality_from_pincode(pincode)
    subject_template, body_template = get_simple_template()
    
    recipients = [{
        'email': recipient_email,
        'name': recipient_name,
        'pincode': pincode,
        'locality': locality
    }]
    
    result = email_service.send_personalized_emails(
        recipients=recipients,
        subject=subject_template,
        template=body_template
    )
    
    return result['results'][0] if result['results'] else {'status': 'error', 'message': 'Unknown error'}

def send_custom_email(recipients_data: List[Dict], subject: str, template: str) -> Dict:
    """
    Send custom emails with any template
    
    Example usage in Flask admin:
        recipients = [
            {'email': 'user1@example.com', 'name': 'John', 'pincode': '110001'},
            {'email': 'user2@example.com', 'name': 'Jane', 'pincode': '400001'}
        ]
        subject = "Important Update - {name}"
        template = "Dear {name}, we have updates for clinical trials in {locality}..."
        
        result = send_custom_email(recipients, subject, template)
        flash(f"Sent {result['success_count']} emails successfully", 'success')
    """
    # Add locality to each recipient
    for recipient in recipients_data:
        if 'locality' not in recipient and 'pincode' in recipient:
            recipient['locality'] = get_locality_from_pincode(recipient['pincode'])
    
    return email_service.send_personalized_emails(
        recipients=recipients_data,
        subject=subject,
        template=template
    )
