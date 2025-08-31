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
    """Initialize database with 20 diverse sample users for clinical trial interest"""
    sample_users = [
        # Eligible participants - various cities and conditions
        {
            'name': 'Rajesh Kumar',
            'email': 'rajesh.kumar@gmail.com',
            'mobile': '9845123456',
            'pincode': '560034',  # Bangalore - eligible
            'age': 42,
            'health_info': 'Type 2 diabetes managed with metformin. HbA1c levels stable. Regular exercise and diet control.',
            'is_eligible': True
        },
        {
            'name': 'Priya Sharma',
            'email': 'priya.sharma@outlook.com',
            'mobile': '9876543210',
            'pincode': '110025',  # Delhi - eligible
            'age': 34,
            'health_info': 'Hypertension controlled with ACE inhibitors. No other significant medical history.',
            'is_eligible': True
        },
        {
            'name': 'Arjun Reddy',
            'email': 'arjun.reddy@yahoo.com',
            'mobile': '9988776655',
            'pincode': '500032',  # Hyderabad - eligible
            'age': 28,
            'health_info': 'Generally healthy. Occasional headaches. Family history of cardiovascular disease.',
            'is_eligible': True
        },
        {
            'name': 'Meera Iyer',
            'email': 'meera.iyer@rediffmail.com',
            'mobile': '9123456789',
            'pincode': '600028',  # Chennai - eligible
            'age': 51,
            'health_info': 'Rheumatoid arthritis treated with methotrexate. Joint pain well controlled.',
            'is_eligible': True
        },
        {
            'name': 'Vikram Singh',
            'email': 'vikram.singh@hotmail.com',
            'mobile': '9765432108',
            'pincode': '400021',  # Mumbai - eligible
            'age': 39,
            'health_info': 'Asthma since childhood. Uses inhaled corticosteroids. No recent exacerbations.',
            'is_eligible': True
        },
        {
            'name': 'Anjali Gupta',
            'email': 'anjali.gupta@gmail.com',
            'mobile': '9654321078',
            'pincode': '700019',  # Kolkata - eligible
            'age': 46,
            'health_info': 'Hypothyroidism on levothyroxine replacement. Thyroid levels within normal range.',
            'is_eligible': True
        },
        {
            'name': 'Sanjay Patel',
            'email': 'sanjay.patel@yahoo.in',
            'mobile': '9543210987',
            'pincode': '380015',  # Ahmedabad - eligible
            'age': 33,
            'health_info': 'No major medical conditions. Occasional back pain from desk job. Takes vitamin D supplements.',
            'is_eligible': True
        },
        {
            'name': 'Kavya Nair',
            'email': 'kavya.nair@gmail.com',
            'mobile': '9432109876',
            'pincode': '682020',  # Kochi - eligible
            'age': 29,
            'health_info': 'PCOS diagnosed 3 years ago. Managed with lifestyle changes and metformin.',
            'is_eligible': True
        },
        {
            'name': 'Rahul Joshi',
            'email': 'rahul.joshi@outlook.com',
            'mobile': '9321098765',
            'pincode': '411014',  # Pune - eligible
            'age': 37,
            'health_info': 'High cholesterol managed with atorvastatin. Regular cardiovascular checkups.',
            'is_eligible': True
        },
        {
            'name': 'Sneha Desai',
            'email': 'sneha.desai@rediffmail.com',
            'mobile': '9210987654',
            'pincode': '302017',  # Jaipur - eligible
            'age': 44,
            'health_info': 'Migraine episodes 2-3 times per month. Takes sumatriptan as needed.',
            'is_eligible': True
        },
        {
            'name': 'Arun Krishnan',
            'email': 'arun.krishnan@gmail.com',
            'mobile': '9109876543',
            'pincode': '560001',  # Bangalore - eligible
            'age': 55,
            'health_info': 'Sleep apnea using CPAP machine. Blood pressure controlled with medication.',
            'is_eligible': True
        },
        {
            'name': 'Divya Agarwal',
            'email': 'divya.agarwal@yahoo.com',
            'mobile': '9098765432',
            'pincode': '201301',  # Noida - eligible
            'age': 31,
            'health_info': 'Irritable bowel syndrome managed with diet modifications. No other conditions.',
            'is_eligible': True
        },
        {
            'name': 'Kiran Kumar',
            'email': 'kiran.kumar@hotmail.com',
            'mobile': '8987654321',
            'pincode': '226010',  # Lucknow - eligible
            'age': 48,
            'health_info': 'Osteoarthritis in knee joints. Takes NSAIDs occasionally for pain relief.',
            'is_eligible': True
        },
        
        # Ineligible participants - various reasons
        {
            'name': 'Ravi Gupta',
            'email': 'ravi.gupta@gmail.com',
            'mobile': '8876543210',
            'pincode': '999999',  # Invalid pincode area
            'age': 35,
            'health_info': 'Generally good health. No chronic conditions. Regular exercise routine.',
            'is_eligible': False
        },
        {
            'name': 'Neha Kapoor',
            'email': 'neha.kapoor@outlook.com',
            'mobile': '8765432109',
            'pincode': '110001',  # Delhi - eligible area
            'age': 17,  # Too young
            'health_info': 'Healthy college student. No medical issues. Active lifestyle.',
            'is_eligible': False
        },
        {
            'name': 'Suresh Malhotra',
            'email': 'suresh.malhotra@yahoo.com',
            'mobile': '8654321098',
            'pincode': '400001',  # Mumbai - eligible area
            'age': 52,
            'health_info': 'Currently undergoing chemotherapy for colon cancer. Started treatment 2 months ago.',
            'is_eligible': False
        },
        {
            'name': 'Pooja Sharma',
            'email': 'pooja.sharma@rediffmail.com',
            'mobile': '8543210987',
            'pincode': '560001',  # Bangalore - eligible area
            'age': 26,
            'health_info': 'Currently pregnant, second trimester. No complications so far.',
            'is_eligible': False
        },
        {
            'name': 'Manish Agarwal',
            'email': 'manish.agarwal@gmail.com',
            'mobile': '8432109876',
            'pincode': '800020',  # Patna - eligible area
            'age': 88,  # Too old
            'health_info': 'Multiple comorbidities including diabetes, hypertension, and heart disease.',
            'is_eligible': False
        },
        {
            'name': 'Sunita Reddy',
            'email': 'sunita.reddy@hotmail.com',
            'mobile': '8321098765',
            'pincode': '500001',  # Hyderabad - eligible area
            'age': 40,
            'health_info': 'Kidney failure on dialysis three times per week. Awaiting transplant.',
            'is_eligible': False
        },
        {
            'name': 'Deepak Verma',
            'email': 'deepak.verma@yahoo.in',
            'mobile': '8210987654',
            'pincode': '123456',  # Invalid pincode format/area
            'age': 32,
            'health_info': 'No major health issues. Occasional seasonal allergies managed with antihistamines.',
            'is_eligible': False
        }
    ]
    
    for user_data in sample_users:
        user = UserSubmission(**user_data)
        db.session.add(user)
    
    db.session.commit()
    print("Sample data initialized successfully!")
