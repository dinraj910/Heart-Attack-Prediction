#!/usr/bin/env python3
"""
Test the deployed Heart Disease Prediction API
"""
import requests
import json
import re

# Test data for prediction
test_data = {
    'age': 55,
    'gender': 'Male',
    'diabetes': 'on',
    'hypertension': 'on',
    'obesity': 'on',
    'smoking': 'on',
    'alcohol': '',
    'physical_activity': 1,
    'diet_score': 3,
    'cholesterol': 280,
    'triglyceride': 200,
    'ldl': 160,
    'hdl': 35,
    'systolic_bp': 160,
    'diastolic_bp': 100,
    'air_pollution': 2,
    'family_history': 'on',
    'stress_level': 8,
    'healthcare': 'Rural',
    'heart_attack_history': '',
    'emergency_time': 300,
    'annual_income': 300000,
    'health_insurance': ''
}

print("🧪 Testing Heart Disease Prediction API...")
print(f"📊 Test data: Age {test_data['age']}, Gender {test_data['gender']}")
print(f"🔴 High risk factors: Diabetes ✓, Hypertension ✓, Obesity ✓, Smoking ✓, Family History ✓")

try:
    # Test the prediction endpoint
    url = "https://web-production-3385.up.railway.app/predict"
    response = requests.post(url, data=test_data)
    
    if response.status_code == 200:
        print("✅ API request successful!")
        
        # Check if the response contains the result page
        if "Risk Score:" in response.text or "risk-score" in response.text:
            print("✅ Found risk score in response")
            # Try multiple patterns to extract risk score
            patterns = [
                r'Risk Score:\s*(\d+(?:\.\d+)?)%',
                r'risk-score["\']>\s*(\d+(?:\.\d+)?)%',
                r'(\d+(?:\.\d+)?)%\s*Risk',
                r'score.*?(\d+(?:\.\d+)?)%'
            ]
            
            risk_score = None
            for pattern in patterns:
                risk_match = re.search(pattern, response.text, re.IGNORECASE)
                if risk_match:
                    risk_score = float(risk_match.group(1))
                    print(f"🎯 Risk Score found: {risk_score}% (pattern: {pattern})")
                    break
            
            if risk_score:
                if risk_score == 50.0:
                    print("❌ ERROR: Still getting default 50% risk score!")
                    print("   The model is not loading properly on Railway")
                else:
                    print(f"✅ SUCCESS: Model is working! Risk score: {risk_score}%")
                    if risk_score > 60:
                        print("🔴 HIGH RISK detected (as expected with these factors)")
                    elif risk_score > 40:
                        print("🟡 MODERATE RISK detected")
                    else:
                        print("🟢 LOW RISK detected")
            else:
                print("❌ Could not extract risk score with any pattern")
                print("Searching for '50' or 'Risk' in response...")
                if "50" in response.text:
                    print("⚠️  Found '50' in response - might be default fallback")
                print("Response preview:", response.text[:1000])
        else:
            print("❌ Response doesn't contain risk score indicators")
            print("Searching for common terms...")
            if "error" in response.text.lower():
                print("⚠️  Found 'error' in response")
            if "model" in response.text.lower():
                print("⚠️  Found 'model' in response")
            if "Unable" in response.text:
                print("⚠️  Found 'Unable' in response")
            print("Response preview:", response.text[:1000])
    else:
        print(f"❌ API request failed with status code: {response.status_code}")
        print("Response:", response.text[:500])
        
except Exception as e:
    print(f"❌ Error testing API: {e}")

print("\n🏁 API test completed!")