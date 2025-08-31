-- Clinical Trial Interest Database - Sample Data
-- 20 diverse mock user entries with realistic information

-- Clear existing data (optional)
-- DELETE FROM user_submission;

-- Insert 20 sample user entries
INSERT INTO user_submission (name, email, mobile, pincode, age, health_info, is_eligible, email_sent) VALUES

-- Eligible Participants (13 users)
('Rajesh Kumar', 'rajesh.kumar@gmail.com', '9845123456', '560034', 42, 'Type 2 diabetes managed with metformin. HbA1c levels stable. Regular exercise and diet control.', true, false),

('Priya Sharma', 'priya.sharma@outlook.com', '9876543210', '110025', 34, 'Hypertension controlled with ACE inhibitors. No other significant medical history.', true, false),

('Arjun Reddy', 'arjun.reddy@yahoo.com', '9988776655', '500032', 28, 'Generally healthy. Occasional headaches. Family history of cardiovascular disease.', true, false),

('Meera Iyer', 'meera.iyer@rediffmail.com', '9123456789', '600028', 51, 'Rheumatoid arthritis treated with methotrexate. Joint pain well controlled.', true, false),

('Vikram Singh', 'vikram.singh@hotmail.com', '9765432108', '400021', 39, 'Asthma since childhood. Uses inhaled corticosteroids. No recent exacerbations.', true, false),

('Anjali Gupta', 'anjali.gupta@gmail.com', '9654321078', '700019', 46, 'Hypothyroidism on levothyroxine replacement. Thyroid levels within normal range.', true, false),

('Sanjay Patel', 'sanjay.patel@yahoo.in', '9543210987', '380015', 33, 'No major medical conditions. Occasional back pain from desk job. Takes vitamin D supplements.', true, false),

('Kavya Nair', 'kavya.nair@gmail.com', '9432109876', '682020', 29, 'PCOS diagnosed 3 years ago. Managed with lifestyle changes and metformin.', true, false),

('Rahul Joshi', 'rahul.joshi@outlook.com', '9321098765', '411014', 37, 'High cholesterol managed with atorvastatin. Regular cardiovascular checkups.', true, false),

('Sneha Desai', 'sneha.desai@rediffmail.com', '9210987654', '302017', 44, 'Migraine episodes 2-3 times per month. Takes sumatriptan as needed.', true, false),

('Arun Krishnan', 'arun.krishnan@gmail.com', '9109876543', '560001', 55, 'Sleep apnea using CPAP machine. Blood pressure controlled with medication.', true, false),

('Divya Agarwal', 'divya.agarwal@yahoo.com', '9098765432', '201301', 31, 'Irritable bowel syndrome managed with diet modifications. No other conditions.', true, false),

('Kiran Kumar', 'kiran.kumar@hotmail.com', '8987654321', '226010', 48, 'Osteoarthritis in knee joints. Takes NSAIDs occasionally for pain relief.', true, false),

-- Ineligible Participants (7 users)
('Ravi Gupta', 'ravi.gupta@gmail.com', '8876543210', '999999', 35, 'Generally good health. No chronic conditions. Regular exercise routine.', false, false),

('Neha Kapoor', 'neha.kapoor@outlook.com', '8765432109', '110001', 17, 'Healthy college student. No medical issues. Active lifestyle.', false, false),

('Suresh Malhotra', 'suresh.malhotra@yahoo.com', '8654321098', '400001', 52, 'Currently undergoing chemotherapy for colon cancer. Started treatment 2 months ago.', false, false),

('Pooja Sharma', 'pooja.sharma@rediffmail.com', '8543210987', '560001', 26, 'Currently pregnant, second trimester. No complications so far.', false, false),

('Manish Agarwal', 'manish.agarwal@gmail.com', '8432109876', '800020', 88, 'Multiple comorbidities including diabetes, hypertension, and heart disease.', false, false),

('Sunita Reddy', 'sunita.reddy@hotmail.com', '8321098765', '500001', 40, 'Kidney failure on dialysis three times per week. Awaiting transplant.', false, false),

('Deepak Verma', 'deepak.verma@yahoo.in', '8210987654', '123456', 32, 'No major health issues. Occasional seasonal allergies managed with antihistamines.', false, false);

-- Summary of data:
-- Total entries: 20
-- Eligible participants: 13 (65%)
-- Ineligible participants: 7 (35%)
-- 
-- Pincode distribution:
-- Bangalore (56xxxx, 57xxxx): 2 users
-- Delhi (11xxxx): 2 users  
-- Mumbai (40xxxx): 2 users
-- Chennai (60xxxx): 1 user
-- Hyderabad (50xxxx): 2 users
-- Kolkata (70xxxx): 1 user
-- Ahmedabad (38xxxx): 1 user
-- Kochi (68xxxx): 1 user
-- Pune (41xxxx): 1 user
-- Jaipur (30xxxx): 1 user
-- Noida (20xxxx): 1 user
-- Lucknow (22xxxx): 1 user
-- Patna (80xxxx): 1 user
-- Invalid areas: 3 users
--
-- Age distribution:
-- 18-30: 4 users
-- 31-45: 9 users  
-- 46-60: 6 users
-- 61+: 1 user
--
-- Common health conditions represented:
-- Diabetes, Hypertension, Asthma, Arthritis, PCOS, Thyroid disorders,
-- Migraine, Sleep apnea, IBS, High cholesterol
--
-- Ineligibility reasons:
-- Age < 18: 1 user
-- Age > 85: 1 user  
-- Invalid pincode area: 2 users
-- Health exclusions (pregnancy, cancer, kidney failure): 3 users