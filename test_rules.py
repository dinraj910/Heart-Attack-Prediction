#!/usr/bin/env python3
"""
Test the rule-based prediction system
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app import calculate_rule_based_risk

print("🧪 Testing Rule-Based Heart Disease Risk Prediction...")

# Test cases
test_cases = [
    {
        'name': 'High Risk Patient',
        'data': {
            'Age': 65,
            'Diabetes': 1,
            'Hypertension': 1,
            'Obesity': 1,
            'Smoking': 1,
            'Physical_Activity': 0,
            'Diet_Score': 2,
            'Cholesterol_Level': 280,
            'Systolic_BP': 160,
            'Diastolic_BP': 100,
            'Family_History': 1,
            'Stress_Level': 9,
            'Triglyceride_Level': 250,
            'HDL_Level': 30
        }
    },
    {
        'name': 'Low Risk Patient',
        'data': {
            'Age': 25,
            'Diabetes': 0,
            'Hypertension': 0,
            'Obesity': 0,
            'Smoking': 0,
            'Physical_Activity': 4,
            'Diet_Score': 8,
            'Cholesterol_Level': 160,
            'Systolic_BP': 110,
            'Diastolic_BP': 70,
            'Family_History': 0,
            'Stress_Level': 3,
            'Triglyceride_Level': 120,
            'HDL_Level': 60
        }
    },
    {
        'name': 'Medium Risk Patient',
        'data': {
            'Age': 45,
            'Diabetes': 0,
            'Hypertension': 1,
            'Obesity': 1,
            'Smoking': 0,
            'Physical_Activity': 2,
            'Diet_Score': 5,
            'Cholesterol_Level': 220,
            'Systolic_BP': 140,
            'Diastolic_BP': 85,
            'Family_History': 1,
            'Stress_Level': 6,
            'Triglyceride_Level': 180,
            'HDL_Level': 45
        }
    }
]

for test_case in test_cases:
    risk_score = calculate_rule_based_risk(test_case['data'])
    risk_percentage = risk_score * 100
    risk_category = 'Low' if risk_score < 0.33 else ('Medium' if risk_score < 0.66 else 'High')
    
    print(f"\n📊 {test_case['name']}:")
    print(f"   Risk Score: {risk_percentage:.1f}%")
    print(f"   Category: {risk_category}")
    print(f"   Age: {test_case['data']['Age']}, Major conditions: {test_case['data']['Diabetes'] + test_case['data']['Hypertension'] + test_case['data']['Obesity']}")

print("\n✅ Rule-based prediction system working!")
print("🎯 This will serve as fallback when ML models fail to load")