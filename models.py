from app import db
from datetime import datetime
import re

class UserSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    health_info = db.Column(db.Text, nullable=False)
    is_eligible = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    email_sent = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<UserSubmission {self.name}>'
    
    @staticmethod
    def validate_pincode(pincode):
        """Validate pincode format (6 digits)"""
        return bool(re.match(r'^\d{6}$', pincode))
    
    @staticmethod
    def check_eligibility(age, pincode):
        """Check if user is eligible for clinical trials"""
        return age >= 18 and UserSubmission.validate_pincode(pincode)

def check_clinical_trial_eligibility(age, pincode, health_info, mobile=None, additional_checks=None):
    """
    Comprehensive eligibility check for clinical trial participation
    
    Args:
        age (int): Participant's age
        pincode (str): Participant's pincode
        health_info (str): Health information provided
        mobile (str, optional): Mobile number for additional validation
        additional_checks (dict, optional): Additional criteria to check
    
    Returns:
        tuple: (is_eligible: bool, reasons: list)
               is_eligible: True if participant meets all criteria
               reasons: List of strings explaining eligibility issues (empty if eligible)
    """
    reasons = []
    
    # Age validation
    if age < 18:
        reasons.append("Participants must be at least 18 years old")
    elif age > 85:
        reasons.append("Participants must be 85 years old or younger for safety considerations")
    
    # Pincode validation - format check
    if not re.match(r'^\d{6}$', str(pincode)):
        reasons.append("Pincode must be a valid 6-digit number")
    else:
        # Pincode validation - allowed regions
        allowed_pincode_prefixes = [
            '11',  # Delhi
            '40',  # Mumbai
            '56',  # Bangalore
            '57',  # Bangalore extended
            '60',  # Chennai
            '70',  # Kolkata
            '50',  # Hyderabad
            '38',  # Ahmedabad
            '20',  # Ghaziabad/Noida
            '41',  # Pune
            '30',  # Jaipur
            '22',  # Lucknow
            '12',  # Gurgaon/Faridabad
            '14',  # Chandigarh
            '16',  # Chandigarh extended
            '15',  # Punjab
            '80',  # Patna
            '75',  # Bhubaneswar
            '64',  # Coimbatore
            '62',  # Madurai
            '68',  # Kochi
        ]
        
        pincode_prefix = str(pincode)[:2]
        if pincode_prefix not in allowed_pincode_prefixes:
            reasons.append(f"Clinical trials are not currently available in your area (pincode: {pincode})")
    
    # Health information validation
    if not health_info or len(health_info.strip()) < 10:
        reasons.append("Please provide detailed health information (minimum 10 characters)")
    
    # Check for exclusionary health conditions
    exclusionary_keywords = [
        'pregnant', 'pregnancy', 'breastfeeding', 'nursing',
        'severe mental illness', 'psychosis', 'schizophrenia',
        'active cancer', 'chemotherapy', 'radiation therapy',
        'organ transplant', 'immunocompromised', 'HIV positive',
        'severe liver disease', 'kidney failure', 'dialysis',
        'recent surgery', 'hospitalized currently'
    ]
    
    health_info_lower = health_info.lower()
    for keyword in exclusionary_keywords:
        if keyword in health_info_lower:
            reasons.append(f"Current health status may require specialized medical evaluation before trial participation")
            break
    
    # Mobile number validation (if provided)
    if mobile and not re.match(r'^\d{10}$', str(mobile)):
        reasons.append("Please provide a valid 10-digit mobile number")
    
    # Additional custom checks
    if additional_checks:
        if 'min_age' in additional_checks and age < additional_checks['min_age']:
            reasons.append(f"This specific trial requires participants to be at least {additional_checks['min_age']} years old")
        
        if 'max_age' in additional_checks and age > additional_checks['max_age']:
            reasons.append(f"This specific trial requires participants to be {additional_checks['max_age']} years old or younger")
        
        if 'required_conditions' in additional_checks:
            required_conditions = additional_checks['required_conditions']
            if not any(condition.lower() in health_info_lower for condition in required_conditions):
                reasons.append(f"This trial requires participants with specific conditions: {', '.join(required_conditions)}")
        
        if 'excluded_medications' in additional_checks:
            excluded_meds = additional_checks['excluded_medications']
            for med in excluded_meds:
                if med.lower() in health_info_lower:
                    reasons.append(f"Current medication ({med}) may interfere with trial participation")
    
    # Determine overall eligibility
    is_eligible = len(reasons) == 0
    
    return is_eligible, reasons

def get_eligibility_message(is_eligible, reasons):
    """
    Generate user-friendly eligibility messages
    
    Args:
        is_eligible (bool): Whether the participant is eligible
        reasons (list): List of eligibility issues
    
    Returns:
        tuple: (message_type: str, message: str)
               message_type: 'success', 'warning', or 'error'
               message: User-friendly message
    """
    if is_eligible:
        return 'success', (
            "Congratulations! You meet our initial eligibility criteria for clinical trial participation. "
            "Our clinical research team will review your information and contact you within 5-7 business days "
            "to discuss specific trials that may be suitable for you."
        )
    
    elif len(reasons) == 1 and 'area' in reasons[0]:
        # Only issue is location
        return 'warning', (
            f"{reasons[0]}. We are continuously expanding our trial locations. "
            "Please check back in the future or contact us if you're willing to travel to a nearby location."
        )
    
    elif len(reasons) == 1 and 'health status' in reasons[0]:
        # Only issue is health-related
        return 'warning', (
            f"{reasons[0]}. This doesn't disqualify you from all trials. "
            "Our medical team will review your case individually and may contact you "
            "for trials with different eligibility criteria."
        )
    
    else:
        # Multiple issues or serious eligibility problems
        reason_text = '; '.join(reasons)
        return 'error', (
            f"We're unable to proceed with your application at this time. {reason_text}. "
            "Please contact our clinical trials information center at 1-800-TRIALS-1 "
            "if you have questions about eligibility requirements."
        )

def init_sample_data():
    """Initialize database with sample data"""
    sample_users = [
        {
            'name': 'John Smith',
            'email': 'john.smith@email.com',
            'mobile': '9876543210',
            'pincode': '110001',
            'age': 45,
            'health_info': 'No major health issues. Regular checkups.',
            'is_eligible': True
        },
        {
            'name': 'Sarah Johnson',
            'email': 'sarah.j@email.com',
            'mobile': '9876543211',
            'pincode': '400001',
            'age': 32,
            'health_info': 'Diabetes Type 2, well controlled.',
            'is_eligible': True
        },
        {
            'name': 'Michael Brown',
            'email': 'michael.brown@email.com',
            'mobile': '9876543212',
            'pincode': '560001',
            'age': 28,
            'health_info': 'Hypertension, on medication.',
            'is_eligible': True
        },
        {
            'name': 'Emily Davis',
            'email': 'emily.davis@email.com',
            'mobile': '9876543213',
            'pincode': '600001',
            'age': 55,
            'health_info': 'Arthritis, mild symptoms.',
            'is_eligible': True
        },
        {
            'name': 'David Wilson',
            'email': 'david.wilson@email.com',
            'mobile': '9876543214',
            'pincode': '700001',
            'age': 41,
            'health_info': 'No known allergies or conditions.',
            'is_eligible': True
        },
        {
            'name': 'Lisa Anderson',
            'email': 'lisa.anderson@email.com',
            'mobile': '9876543215',
            'pincode': '500001',
            'age': 36,
            'health_info': 'Asthma, controlled with inhaler.',
            'is_eligible': True
        },
        {
            'name': 'Robert Taylor',
            'email': 'robert.taylor@email.com',
            'mobile': '9876543216',
            'pincode': '380001',
            'age': 50,
            'health_info': 'High cholesterol, on statins.',
            'is_eligible': True
        },
        {
            'name': 'Jennifer Martinez',
            'email': 'jennifer.martinez@email.com',
            'mobile': '9876543217',
            'pincode': '201001',
            'age': 29,
            'health_info': 'PCOS, regular monitoring.',
            'is_eligible': True
        },
        {
            'name': 'William Garcia',
            'email': 'william.garcia@email.com',
            'mobile': '9876543218',
            'pincode': '411001',
            'age': 38,
            'health_info': 'No significant medical history.',
            'is_eligible': True
        },
        {
            'name': 'Amanda Rodriguez',
            'email': 'amanda.rodriguez@email.com',
            'mobile': '9876543219',
            'pincode': '302001',
            'age': 43,
            'health_info': 'Migraine, occasional episodes.',
            'is_eligible': True
        },
        {
            'name': 'James Lee',
            'email': 'james.lee@email.com',
            'mobile': '9876543220',
            'pincode': '226001',
            'age': 31,
            'health_info': 'Thyroid disorder, on medication.',
            'is_eligible': True
        },
        {
            'name': 'Michelle White',
            'email': 'michelle.white@email.com',
            'mobile': '9876543221',
            'pincode': '121001',
            'age': 47,
            'health_info': 'Osteoporosis, taking supplements.',
            'is_eligible': True
        },
        {
            'name': 'Christopher Hall',
            'email': 'christopher.hall@email.com',
            'mobile': '9876543222',
            'pincode': '141001',
            'age': 26,
            'health_info': 'Allergic rhinitis, seasonal.',
            'is_eligible': True
        },
        {
            'name': 'Stephanie Young',
            'email': 'stephanie.young@email.com',
            'mobile': '9876543223',
            'pincode': '160001',
            'age': 39,
            'health_info': 'Anxiety disorder, managed well.',
            'is_eligible': True
        },
        {
            'name': 'Daniel King',
            'email': 'daniel.king@email.com',
            'mobile': '9876543224',
            'pincode': '151001',
            'age': 52,
            'health_info': 'Sleep apnea, uses CPAP machine.',
            'is_eligible': True
        },
        {
            'name': 'Karen Wright',
            'email': 'karen.wright@email.com',
            'mobile': '9876543225',
            'pincode': '800001',
            'age': 34,
            'health_info': 'IBS, dietary management.',
            'is_eligible': True
        },
        {
            'name': 'Matthew Lopez',
            'email': 'matthew.lopez@email.com',
            'mobile': '9876543226',
            'pincode': '751001',
            'age': 44,
            'health_info': 'No major health concerns.',
            'is_eligible': True
        },
        {
            'name': 'Nancy Hill',
            'email': 'nancy.hill@email.com',
            'mobile': '9876543227',
            'pincode': '641001',
            'age': 17,
            'health_info': 'Healthy teenager, no issues.',
            'is_eligible': False
        },
        {
            'name': 'Andrew Scott',
            'email': 'andrew.scott@email.com',
            'mobile': '9876543228',
            'pincode': '620001',
            'age': 25,
            'health_info': 'Depression, on antidepressants.',
            'is_eligible': True
        },
        {
            'name': 'Patricia Green',
            'email': 'patricia.green@email.com',
            'mobile': '9876543229',
            'pincode': '682001',
            'age': 48,
            'health_info': 'Fibromyalgia, pain management.',
            'is_eligible': True
        }
    ]
    
    for user_data in sample_users:
        user = UserSubmission(**user_data)
        db.session.add(user)
    
    db.session.commit()
    print("Sample data initialized successfully!")
