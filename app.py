from flask import Flask, render_template, request, redirect, url_for, jsonify
import joblib
import numpy as np
import pandas as pd
import os
import sys

app = Flask(__name__)

# Add debug info for hosting platforms
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")

# Check if models directory exists
if os.path.exists('models'):
    print(f"Models directory exists. Contents: {os.listdir('models')}")
else:
    print("❌ Models directory does not exist!")

# Production-ready model loading with extensive error handling
model = None
try:
    # Try multiple possible paths for the model
    possible_paths = [
        'heart_disease_pipeline.pkl',  # Root directory (for Railway)
        os.path.join(os.path.dirname(__file__), 'models', 'heart_disease_pipeline.pkl'),
        os.path.join('models', 'heart_disease_pipeline.pkl'),
        'models/heart_disease_pipeline.pkl',
        './models/heart_disease_pipeline.pkl'
    ]
    
    print("🔍 Searching for model file...")
    for i, model_path in enumerate(possible_paths):
        print(f"  Path {i+1}: {model_path} - {'EXISTS' if os.path.exists(model_path) else 'NOT FOUND'}")
        if os.path.exists(model_path):
            try:
                model = joblib.load(model_path)
                print(f"✅ Model loaded successfully from: {model_path}")
                print(f"✅ Model type: {type(model)}")
                break
            except Exception as load_error:
                print(f"❌ Failed to load from {model_path}: {load_error}")
    
    if model is None:
        print("❌ Model file not found in any expected location")
        print("Available files in current directory:", os.listdir('.'))
        if os.path.exists('models'):
            print("Files in models directory:", os.listdir('models'))
        
except Exception as e:
    print(f"❌ Error during model loading: {e}")
    import traceback
    traceback.print_exc()

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'python_version': sys.version,
        'cwd': os.getcwd()
    })

# Simple test route
@app.route('/test')
def test():
    return "✅ Flask app is running! Model loaded: " + str(model is not None)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Extract all form data and convert to proper numeric format
        state_value = request.form.get('state', 'Delhi')
        # If Kerala is selected, map it to Tamil Nadu for the model
        if state_value == 'Kerala':
            state_value = 'Tamil Nadu'
            
        patient_data = {
            'Patient_ID': 1,  # Default Patient ID
            'State_Name': state_value,
            'Age': int(request.form.get('age', 45)),
            'Gender': 1 if request.form.get('gender', 'Male') == 'Male' else 0,  # Convert to numeric
            'Diabetes': 1 if request.form.get('diabetes') else 0,  # Convert to numeric
            'Hypertension': 1 if request.form.get('hypertension') else 0,  # Convert to numeric
            'Obesity': 1 if request.form.get('obesity') else 0,  # Convert to numeric
            'Smoking': 1 if request.form.get('smoking') else 0,  # Convert to numeric
            'Alcohol_Consumption': 1 if request.form.get('alcohol') else 0,  # Convert to numeric
            'Physical_Activity': int(request.form.get('physical_activity', 2)),
            'Diet_Score': int(request.form.get('diet_score', 5)),
            'Cholesterol_Level': int(request.form.get('cholesterol', 200)),
            'Triglyceride_Level': int(request.form.get('triglyceride', 150)),
            'LDL_Level': int(request.form.get('ldl', 100)),
            'HDL_Level': int(request.form.get('hdl', 50)),
            'Systolic_BP': int(request.form.get('systolic_bp', 120)),
            'Diastolic_BP': int(request.form.get('diastolic_bp', 80)),
            'Air_Pollution_Exposure': int(request.form.get('air_pollution', 1)),
            'Family_History': 1 if request.form.get('family_history') else 0,  # Convert to numeric
            'Stress_Level': int(request.form.get('stress_level', 5)),
            'Healthcare_Access': 1 if request.form.get('healthcare', 'Urban') == 'Urban' else 0,  # Convert to numeric
            'Heart_Attack_History': 1 if request.form.get('heart_attack_history') else 0,  # Convert to numeric
            'Emergency_Response_Time': int(request.form.get('emergency_time', 200)),
            'Annual_Income': int(request.form.get('annual_income', 500000)),
            'Health_Insurance': 1 if request.form.get('health_insurance') else 0  # Convert to numeric
        }
        
        # Create DataFrame with all features including Patient_ID (exact column names from original dataset)
        feature_columns = ['Patient_ID', 'State_Name', 'Age', 'Gender', 'Diabetes', 'Hypertension', 'Obesity', 
                          'Smoking', 'Alcohol_Consumption', 'Physical_Activity', 'Diet_Score',
                          'Cholesterol_Level', 'Triglyceride_Level', 'LDL_Level', 'HDL_Level',
                          'Systolic_BP', 'Diastolic_BP', 'Air_Pollution_Exposure', 'Family_History',
                          'Stress_Level', 'Healthcare_Access', 'Heart_Attack_History', 
                          'Emergency_Response_Time', 'Annual_Income', 'Health_Insurance']
        
        # Create input array in the correct order
        input_data = [patient_data[col] for col in feature_columns]
        X = pd.DataFrame([input_data], columns=feature_columns)
        
        # Check if model is loaded
        if model is None:
            return render_template('result.html',
                                 risk_score=50,
                                 risk_category='Unable to assess',
                                 feature_importance=[('Error', 'Model not loaded - please contact support')])
        
        try:
            # Make prediction
            pred_prob = model.predict_proba(X)[0][1]
            pred_class = model.predict(X)[0]
            risk_category = 'Low' if pred_prob < 0.33 else ('Medium' if pred_prob < 0.66 else 'High')
            
            # Create simple feature importance without SHAP
            feature_importance = [
                ('Age', patient_data['Age']),
                ('Cholesterol Level', patient_data['Cholesterol_Level']),
                ('Blood Pressure', f"{patient_data['Systolic_BP']}/{patient_data['Diastolic_BP']}"),
                ('Family History', 'Yes' if patient_data['Family_History'] else 'No'),
                ('Smoking', 'Yes' if patient_data['Smoking'] else 'No'),
                ('Physical Activity', patient_data['Physical_Activity']),
                ('Stress Level', patient_data['Stress_Level'])
            ]
            
            return render_template('result.html',
                                   risk_score=int(pred_prob*100),
                                   risk_category=risk_category,
                                   feature_importance=feature_importance)
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return render_template('result.html',
                                 risk_score=50,
                                 risk_category='Error',
                                 feature_importance=[('Error', str(e))])
    
    return render_template('predict.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
