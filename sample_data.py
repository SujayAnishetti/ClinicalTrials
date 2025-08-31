"""
Clinical Trial Interest Database - Sample Data Generator

This file contains 20 diverse mock user entries for testing
the clinical trial registration system.
"""

# Python dictionary format for direct use in Flask/Python
SAMPLE_USERS = [
    # Eligible Participants (13 users)
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
    
    # Ineligible Participants (7 users) 
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

# Data summary
DATA_SUMMARY = {
    'total_entries': 20,
    'eligible_count': 13, 
    'ineligible_count': 7,
    'eligibility_rate': 65,
    
    'cities_represented': [
        'Bangalore', 'Delhi', 'Mumbai', 'Chennai', 'Hyderabad',
        'Kolkata', 'Ahmedabad', 'Kochi', 'Pune', 'Jaipur', 
        'Noida', 'Lucknow', 'Patna'
    ],
    
    'age_groups': {
        '18-30': 4,
        '31-45': 9, 
        '46-60': 6,
        '61+': 1
    },
    
    'health_conditions': [
        'Diabetes', 'Hypertension', 'Asthma', 'Arthritis', 'PCOS',
        'Thyroid disorders', 'Migraine', 'Sleep apnea', 'IBS', 
        'High cholesterol', 'Cancer', 'Kidney disease'
    ],
    
    'ineligibility_reasons': {
        'too_young': 1,
        'too_old': 1,
        'invalid_area': 2,
        'health_exclusions': 3
    }
}

def load_sample_data_to_database():
    """
    Function to load sample data into Flask database
    
    Usage:
        from sample_data import load_sample_data_to_database
        load_sample_data_to_database()
    """
    from models import UserSubmission
    from app import db
    
    # Clear existing data (optional)
    # UserSubmission.query.delete()
    
    # Add sample users
    for user_data in SAMPLE_USERS:
        user = UserSubmission(**user_data)
        db.session.add(user)
    
    db.session.commit()
    print(f"Successfully loaded {len(SAMPLE_USERS)} sample users to database")

def get_eligible_users():
    """Get only eligible users from sample data"""
    return [user for user in SAMPLE_USERS if user['is_eligible']]

def get_ineligible_users():
    """Get only ineligible users from sample data"""
    return [user for user in SAMPLE_USERS if not user['is_eligible']]

def get_users_by_city(pincode_prefix):
    """Get users from specific city by pincode prefix"""
    return [user for user in SAMPLE_USERS if user['pincode'].startswith(pincode_prefix)]

def get_users_by_age_range(min_age, max_age):
    """Get users within specific age range"""
    return [user for user in SAMPLE_USERS if min_age <= user['age'] <= max_age]

if __name__ == "__main__":
    print("Clinical Trial Sample Data")
    print("=" * 40)
    print(f"Total users: {DATA_SUMMARY['total_entries']}")
    print(f"Eligible: {DATA_SUMMARY['eligible_count']} ({DATA_SUMMARY['eligibility_rate']}%)")
    print(f"Ineligible: {DATA_SUMMARY['ineligible_count']}")
    print(f"Cities: {len(DATA_SUMMARY['cities_represented'])}")
    print("\nUse load_sample_data_to_database() to load into Flask app")