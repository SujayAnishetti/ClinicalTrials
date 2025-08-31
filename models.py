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
