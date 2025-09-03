from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Regexp
from wtforms.widgets import TextArea

class InterestForm(FlaskForm):
    name = StringField('Full Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    
    mobile = StringField('Mobile Number', validators=[
        DataRequired(message='Mobile number is required'),
        Regexp(r'^\d{10}$', message='Please enter a valid 10-digit mobile number')
    ])
    
    zipcode = StringField('ZIP Code', validators=[
        DataRequired(message='ZIP Code is required'),
        Regexp(r'^\d{5}$', message='Please enter a valid 5-digit ZIP code')
    ])
    
    age = IntegerField('Age', validators=[
        DataRequired(message='Age is required'),
        NumberRange(min=16, max=120, message='Age must be between 16 and 120')
    ])
    
    health_info = TextAreaField('Brief Health Information', validators=[
        DataRequired(message='Health information is required'),
        Length(min=10, max=500, message='Please provide between 10 and 500 characters')
    ], widget=TextArea(), render_kw={"rows": 4, "placeholder": "Please describe your current health status, any medical conditions, medications, or relevant health information..."})
    
    submit = SubmitField('Submit Interest')

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required')
    ], render_kw={"placeholder": "Enter username"})
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ], render_kw={"placeholder": "Enter password"})
    
    submit = SubmitField('Login')

class CellTherapyInterestForm(FlaskForm):
    name = StringField('Full Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    
    mobile = StringField('Mobile Number', validators=[
        DataRequired(message='Mobile number is required'),
        Regexp(r'^\d{10}$', message='Please enter a valid 10-digit mobile number')
    ])
    
    zipcode = StringField('ZIP Code', validators=[
        DataRequired(message='ZIP Code is required'),
        Regexp(r'^\d{5}$', message='Please enter a valid 5-digit ZIP code')
    ])
    
    age = IntegerField('Age', validators=[
        DataRequired(message='Age is required'),
        NumberRange(min=16, max=120, message='Age must be between 16 and 120')
    ])
    
    diagnosis = StringField('Current Diagnosis', validators=[
        DataRequired(message='Diagnosis is required'),
        Length(min=5, max=200, message='Please provide between 5 and 200 characters')
    ], render_kw={"placeholder": "e.g., Hepatocellular Carcinoma, Advanced Liver Cancer, etc."})
    
    current_health_status = TextAreaField('Current Health Status', validators=[
        DataRequired(message='Current health status is required'),
        Length(min=20, max=1000, message='Please provide between 20 and 1000 characters')
    ], widget=TextArea(), render_kw={"rows": 5, "placeholder": "Please describe your current health status, any treatments you've received, current medications, and any relevant medical history..."})
    
    submit = SubmitField('Submit Interest for Cell Therapy')

class AdminSearchForm(FlaskForm):
    search_zipcode = StringField('Search by ZIP Code', render_kw={"placeholder": "Enter ZIP code"})
    
    eligibility_filter = SelectField('Filter by Eligibility', choices=[
        ('', 'All'),
        ('eligible', 'Eligible Only'),
        ('not_eligible', 'Not Eligible Only')
    ])
    
    therapy_filter = SelectField('Filter by Therapy Type', choices=[
        ('', 'All Therapies'),
        ('general', 'General Interest'),
        ('cell_therapy', 'Cell Therapy')
    ])
    
    submit = SubmitField('Search')
