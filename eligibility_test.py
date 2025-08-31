"""
Eligibility Check Function Test Examples

This file demonstrates the clinical trial eligibility checker
with various test cases to show how it works.
"""

from models import check_clinical_trial_eligibility, get_eligibility_message

def test_eligibility_scenarios():
    """Test various eligibility scenarios"""
    
    print("Clinical Trial Eligibility Check - Test Cases")
    print("=" * 60)
    
    # Test Case 1: Eligible participant
    print("\n1. ELIGIBLE PARTICIPANT:")
    is_eligible, reasons = check_clinical_trial_eligibility(
        age=35,
        pincode="560001",  # Bangalore
        health_info="No major health issues. Regular exercise and balanced diet.",
        mobile="9876543210"
    )
    message_type, message = get_eligibility_message(is_eligible, reasons)
    print(f"   Eligible: {is_eligible}")
    print(f"   Message Type: {message_type}")
    print(f"   Message: {message}")
    
    # Test Case 2: Too young
    print("\n2. TOO YOUNG:")
    is_eligible, reasons = check_clinical_trial_eligibility(
        age=17,
        pincode="110001",  # Delhi
        health_info="Healthy teenager, no medical issues.",
        mobile="9876543210"
    )
    message_type, message = get_eligibility_message(is_eligible, reasons)
    print(f"   Eligible: {is_eligible}")
    print(f"   Reasons: {reasons}")
    print(f"   Message Type: {message_type}")
    
    # Test Case 3: Invalid pincode area
    print("\n3. INVALID PINCODE AREA:")
    is_eligible, reasons = check_clinical_trial_eligibility(
        age=45,
        pincode="999999",  # Not in allowed areas
        health_info="Good health, no chronic conditions.",
        mobile="9876543210"
    )
    message_type, message = get_eligibility_message(is_eligible, reasons)
    print(f"   Eligible: {is_eligible}")
    print(f"   Reasons: {reasons}")
    print(f"   Message Type: {message_type}")
    
    # Test Case 4: Health concerns
    print("\n4. HEALTH CONCERNS:")
    is_eligible, reasons = check_clinical_trial_eligibility(
        age=50,
        pincode="400001",  # Mumbai
        health_info="Currently pregnant and taking prenatal vitamins.",
        mobile="9876543210"
    )
    message_type, message = get_eligibility_message(is_eligible, reasons)
    print(f"   Eligible: {is_eligible}")
    print(f"   Reasons: {reasons}")
    print(f"   Message Type: {message_type}")
    
    # Test Case 5: Insufficient health info
    print("\n5. INSUFFICIENT HEALTH INFO:")
    is_eligible, reasons = check_clinical_trial_eligibility(
        age=30,
        pincode="600001",  # Chennai
        health_info="Good",  # Too short
        mobile="9876543210"
    )
    message_type, message = get_eligibility_message(is_eligible, reasons)
    print(f"   Eligible: {is_eligible}")
    print(f"   Reasons: {reasons}")
    
    # Test Case 6: Multiple issues
    print("\n6. MULTIPLE ISSUES:")
    is_eligible, reasons = check_clinical_trial_eligibility(
        age=16,  # Too young
        pincode="999999",  # Invalid area
        health_info="Active cancer treatment",  # Health concern
        mobile="98765"  # Invalid mobile
    )
    message_type, message = get_eligibility_message(is_eligible, reasons)
    print(f"   Eligible: {is_eligible}")
    print(f"   Reasons: {reasons}")
    print(f"   Message Type: {message_type}")
    
    # Test Case 7: With additional checks
    print("\n7. ADDITIONAL CHECKS (Diabetes Trial):")
    additional_checks = {
        'min_age': 25,
        'max_age': 65,
        'required_conditions': ['diabetes', 'type 2', 'blood sugar'],
        'excluded_medications': ['insulin']
    }
    
    is_eligible, reasons = check_clinical_trial_eligibility(
        age=45,
        pincode="110001",
        health_info="Type 2 diabetes controlled with metformin. HbA1c: 7.2%",
        mobile="9876543210",
        additional_checks=additional_checks
    )
    message_type, message = get_eligibility_message(is_eligible, reasons)
    print(f"   Eligible: {is_eligible}")
    print(f"   Reasons: {reasons}")
    print(f"   Message Type: {message_type}")

def show_allowed_pincodes():
    """Show the allowed pincode areas"""
    print("\n\nALLOWED PINCODE AREAS:")
    print("=" * 40)
    
    allowed_areas = {
        '11': 'Delhi',
        '40': 'Mumbai',
        '56': 'Bangalore',
        '57': 'Bangalore Extended',
        '60': 'Chennai',
        '70': 'Kolkata',
        '50': 'Hyderabad',
        '38': 'Ahmedabad',
        '20': 'Ghaziabad/Noida',
        '41': 'Pune',
        '30': 'Jaipur',
        '22': 'Lucknow',
        '12': 'Gurgaon/Faridabad',
        '14': 'Chandigarh',
        '16': 'Chandigarh Extended',
        '15': 'Punjab',
        '80': 'Patna',
        '75': 'Bhubaneswar',
        '64': 'Coimbatore',
        '62': 'Madurai',
        '68': 'Kochi'
    }
    
    for prefix, city in allowed_areas.items():
        print(f"   {prefix}xxxx - {city}")

def show_exclusionary_conditions():
    """Show health conditions that may require special evaluation"""
    print("\n\nEXCLUSIONARY CONDITIONS:")
    print("=" * 40)
    
    conditions = [
        'pregnant', 'pregnancy', 'breastfeeding', 'nursing',
        'severe mental illness', 'psychosis', 'schizophrenia',
        'active cancer', 'chemotherapy', 'radiation therapy',
        'organ transplant', 'immunocompromised', 'HIV positive',
        'severe liver disease', 'kidney failure', 'dialysis',
        'recent surgery', 'hospitalized currently'
    ]
    
    print("   If health info contains any of these keywords:")
    for condition in conditions:
        print(f"   - {condition}")
    print("\n   Note: These don't automatically disqualify, but require medical review.")

if __name__ == "__main__":
    test_eligibility_scenarios()
    show_allowed_pincodes()
    show_exclusionary_conditions()
    
    print("\n\nINTEGRATION NOTES:")
    print("=" * 40)
    print("The eligibility function is integrated into the Flask form route:")
    print("- /interest (POST) - Uses check_clinical_trial_eligibility()")
    print("- /api/check_eligibility (POST) - API endpoint for real-time checks")
    print("- User sees appropriate success/warning/error messages")
    print("- All submissions are saved regardless of eligibility")
    print("- Admin can see eligibility status in dashboard")