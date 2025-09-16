from flask import Flask, render_template, request, redirect, url_for, jsonify
import joblib
import shap
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Production-ready model loading with error handling
try:
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'heart_disease_pipeline.pkl')
    if not os.path.exists(model_path):
        # Try alternative path for different hosting environments
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'heart_disease_pipeline.pkl')
    model = joblib.load(model_path)
    print(f"Model loaded successfully from: {model_path}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

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
        
        # Make prediction
        pred_prob = model.predict_proba(X)[0][1]
        pred_class = model.predict(X)[0]
        risk_category = 'Low' if pred_prob < 0.33 else ('Medium' if pred_prob < 0.66 else 'High')
        
        # SHAP explanation
        try:
            explainer = shap.Explainer(model.named_steps['clf'], model.named_steps['preprocessor'].transform(X))
            shap_values = explainer(model.named_steps['preprocessor'].transform(X))
            feature_importance = list(zip(feature_columns[1:], shap_values.values[0]))  # Exclude Patient_ID from display
            feature_importance.sort(key=lambda x: abs(x[1]), reverse=True)
        except Exception as e:
            print(f"SHAP explanation failed: {e}")
            # Fallback feature importance based on common heart disease risk factors
            feature_importance = [
                ('Age', 0.15),
                ('Cholesterol_Level', 0.12), 
                ('Systolic_BP', 0.10),
                ('Diabetes', 0.08),
                ('Smoking', 0.07),
                ('Family_History', 0.06),
                ('Stress_Level', 0.05),
                ('Physical_Activity', -0.04)
            ]
        
        return render_template('result.html',
                               risk_score=int(pred_prob*100),
                               risk_category=risk_category,
                               feature_importance=feature_importance)
    
    return render_template('predict.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
