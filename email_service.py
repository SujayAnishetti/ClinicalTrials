import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app import db

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

def send_bulk_emails(submissions):
    """Send emails to multiple submissions"""
    
    # Get SMTP configuration from environment variables
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    smtp_username = os.environ.get('SMTP_USERNAME', 'your-email@gmail.com')
    smtp_password = os.environ.get('SMTP_PASSWORD', 'your-app-password')
    from_email = os.environ.get('FROM_EMAIL', smtp_username)
    
    success_count = 0
    error_count = 0
    
    try:
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable security
        server.login(smtp_username, smtp_password)
        
        for submission in submissions:
            try:
                # Generate email content
                subject, html_body = get_email_template(submission.name, submission.pincode)
                
                # Create message
                msg = MIMEMultipart('alternative')
                msg['From'] = from_email
                msg['To'] = submission.email
                msg['Subject'] = subject
                
                # Attach HTML body
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
                
                # Send email
                server.send_message(msg)
                
                # Mark as sent in database
                submission.email_sent = True
                success_count += 1
                
                logging.info(f"Email sent successfully to {submission.email}")
                
            except Exception as e:
                error_count += 1
                logging.error(f"Failed to send email to {submission.email}: {e}")
        
        # Commit database changes
        db.session.commit()
        
        # Close SMTP session
        server.quit()
        
    except Exception as e:
        logging.error(f"SMTP connection error: {e}")
        error_count = len(submissions)
    
    return success_count, error_count
