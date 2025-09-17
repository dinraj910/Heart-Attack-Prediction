from flask import Flask, render_template, request, redirect, url_for, jsonify
import joblib
import numpy as np
import pandas as pd
import os
import sys
import json

app = Flask(__name__)

def calculate_rule_based_risk(patient_data):
    """
    Calculate heart disease risk using evidence-based clinical rules
    Returns risk score between 0.0 and 1.0
    """
    risk_score = 0.0
    
    # Age factor (major risk factor)
    age = patient_data['Age']
    if age >= 65:
        risk_score += 0.25
    elif age >= 55:
        risk_score += 0.15
    elif age >= 45:
        risk_score += 0.10
    elif age >= 35:
        risk_score += 0.05
    
    # Major medical conditions
    if patient_data['Diabetes']:
        risk_score += 0.20  # Diabetes is a major risk factor
    if patient_data['Hypertension']:
        risk_score += 0.15  # High blood pressure
    if patient_data['Obesity']:
        risk_score += 0.10  # Obesity
    
    # Lifestyle factors
    if patient_data['Smoking']:
        risk_score += 0.20  # Smoking is a major risk factor
    if patient_data['Physical_Activity'] <= 1:
        risk_score += 0.10  # Sedentary lifestyle
    
    # Blood pressure values
    systolic = patient_data['Systolic_BP']
    diastolic = patient_data['Diastolic_BP']
    if systolic >= 140 or diastolic >= 90:
        risk_score += 0.15  # Stage 1 hypertension or higher
    elif systolic >= 130 or diastolic >= 80:
        risk_score += 0.08  # Elevated blood pressure
    
    # Cholesterol levels
    cholesterol = patient_data['Cholesterol_Level']
    if cholesterol >= 240:
        risk_score += 0.15  # High cholesterol
    elif cholesterol >= 200:
        risk_score += 0.08  # Borderline high
    
    # Family history
    if patient_data['Family_History']:
        risk_score += 0.12  # Genetic predisposition
    
    # Stress level
    stress = patient_data['Stress_Level']
    if stress >= 8:
        risk_score += 0.08  # High stress
    elif stress >= 6:
        risk_score += 0.04  # Moderate stress
    
    # Diet score (lower is worse)
    diet = patient_data['Diet_Score']
    if diet <= 3:
        risk_score += 0.08  # Poor diet
    elif diet <= 5:
        risk_score += 0.04  # Fair diet
    
    # Cap the risk score at 1.0 (100%)
    risk_score = min(risk_score, 1.0)
    
    # Add some variance based on triglycerides and other factors
    if patient_data.get('Triglyceride_Level', 150) >= 200:
        risk_score += 0.05
    
    if patient_data.get('HDL_Level', 50) < 40:  # Low HDL (good cholesterol)
        risk_score += 0.05
    
    # Ensure minimum risk for very young, healthy individuals
    if age < 30 and risk_score < 0.05:
        risk_score = max(risk_score, 0.05)
    
    # Final cap
    return min(risk_score, 0.95)  # Max 95% risk

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
model_type = "complex"  # Global variable to track model type
try:
    # Try multiple possible paths for the model
    possible_paths = [
        'heart_disease_pipeline.pkl',  # Root directory (for Railway)
        'simple_heart_model.pkl',  # Simple fallback model
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
                
                # Determine model type
                if 'simple' in model_path:
                    model_type = "simple"
                    print("📝 Using simple model (12 features)")
                else:
                    model_type = "complex"
                    print("📝 Using complex model (24 features)")
                break
            except Exception as load_error:
                print(f"❌ Failed to load from {model_path}: {load_error}")
                continue
    
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

@app.route('/reload-model')
def reload_model():
    """Force reload the model - useful for debugging"""
    global model
    
    print("🔄 Forcing model reload...")
    
    model = None
    try:
        possible_paths = [
            'heart_disease_pipeline.pkl',
            'models/heart_disease_pipeline.pkl',
            './models/heart_disease_pipeline.pkl',
            os.path.join('models', 'heart_disease_pipeline.pkl'),
            os.path.join(os.path.dirname(__file__), 'models', 'heart_disease_pipeline.pkl')
        ]
        
        for i, path in enumerate(possible_paths):
            print(f"  Path {i+1}: {path} - {'EXISTS' if os.path.exists(path) else 'NOT FOUND'}")
            if os.path.exists(path):
                try:
                    model = joblib.load(path)
                    print(f"✅ Model reloaded successfully from: {path}")
                    print(f"Model type: {type(model)}")
                    
                    # Test prediction
                    sample_data = {
                        'State_Name': 'Delhi',
                        'Age': 45,
                        'Gender': 'Male',
                        'Diabetes': 1,
                        'Hypertension': 1,
                        'Obesity': 1,
                        'Smoking': 1,
                        'Alcohol_Consumption': 0,
                        'Physical_Activity': 1,
                        'Diet_Score': 3,
                        'Cholesterol_Level': 280,
                        'Triglyceride_Level': 220,
                        'LDL_Level': 160,
                        'HDL_Level': 35,
                        'Systolic_BP': 160,
                        'Diastolic_BP': 100,
                        'Air_Pollution_Exposure': 1,
                        'Family_History': 1,
                        'Stress_Level': 8,
                        'Healthcare_Access': 1,
                        'Heart_Attack_History': 0,
                        'Emergency_Response_Time': 250,
                        'Annual_Income': 400000,
                        'Health_Insurance': 0
                    }
                    
                    test_df = pd.DataFrame([sample_data])
                    pred_prob = model.predict_proba(test_df)[0][1]
                    
                    return f"""
                    <h2>✅ Model Reload Successful!</h2>
                    <p><strong>Model Path:</strong> {path}</p>
                    <p><strong>Model Type:</strong> {type(model)}</p>
                    <p><strong>Test Prediction:</strong> {pred_prob:.4f} ({pred_prob*100:.1f}%)</p>
                    <p><strong>Status:</strong> Model is working correctly!</p>
                    <a href="/predict">Test the prediction form</a>
                    """
                except Exception as load_error:
                    print(f"❌ Failed to reload from {path}: {load_error}")
        
        if model is None:
            return f"""
            <h2>❌ Model Reload Failed</h2>
            <p>No model could be loaded from any path.</p>
            <p><strong>Available files:</strong> {os.listdir('.')}</p>
            <p><strong>Models directory:</strong> {os.listdir('models') if os.path.exists('models') else 'Not found'}</p>
            """
            
    except Exception as e:
        return f"""
        <h2>❌ Model Reload Error</h2>
        <p><strong>Error:</strong> {e}</p>
        <p><strong>Type:</strong> {type(e)}</p>
        """

@app.route('/debug')
def debug():
    """Debug route to check model loading status"""
    debug_info = {
        'model_loaded': model is not None,
        'model_type': str(type(model)) if model else 'None',
        'current_directory': os.getcwd(),
        'files_in_directory': os.listdir('.'),
        'python_version': sys.version
    }
    
    if os.path.exists('models'):
        debug_info['models_directory'] = os.listdir('models')
    else:
        debug_info['models_directory'] = 'Directory not found'
    
    # Check if model files exist
    model_files = {}
    paths_to_check = [
        'heart_disease_pipeline.pkl',
        'models/heart_disease_pipeline.pkl',
        './models/heart_disease_pipeline.pkl'
    ]
    
    for path in paths_to_check:
        model_files[path] = os.path.exists(path)
    
    debug_info['model_file_checks'] = model_files
    
    return f"<pre>{json.dumps(debug_info, indent=2)}</pre>"

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Extract all form data and convert to proper numeric format
        state_value = request.form.get('state', 'Delhi')
        # If Kerala is selected, map it to Tamil Nadu for the model
        if state_value == 'Kerala':
            state_value = 'Tamil Nadu'
            
        patient_data = {
            'State_Name': state_value,
            'Age': int(request.form.get('age', 45)),
            'Gender': request.form.get('gender', 'Male'),  # Keep as string for proper encoding
            'Diabetes': 1 if request.form.get('diabetes') else 0,
            'Hypertension': 1 if request.form.get('hypertension') else 0,
            'Obesity': 1 if request.form.get('obesity') else 0,
            'Smoking': 1 if request.form.get('smoking') else 0,
            'Alcohol_Consumption': 1 if request.form.get('alcohol') else 0,
            'Physical_Activity': int(request.form.get('physical_activity', 2)),
            'Diet_Score': int(request.form.get('diet_score', 5)),
            'Cholesterol_Level': int(request.form.get('cholesterol', 200)),
            'Triglyceride_Level': int(request.form.get('triglyceride', 150)),
            'LDL_Level': int(request.form.get('ldl', 100)),
            'HDL_Level': int(request.form.get('hdl', 50)),
            'Systolic_BP': int(request.form.get('systolic_bp', 120)),
            'Diastolic_BP': int(request.form.get('diastolic_bp', 80)),
            'Air_Pollution_Exposure': int(request.form.get('air_pollution', 1)),
            'Family_History': 1 if request.form.get('family_history') else 0,
            'Stress_Level': int(request.form.get('stress_level', 5)),
            'Healthcare_Access': 1 if request.form.get('healthcare', 'Urban') == 'Urban' else 0,
            'Heart_Attack_History': 1 if request.form.get('heart_attack_history') else 0,
            'Emergency_Response_Time': int(request.form.get('emergency_time', 200)),
            'Annual_Income': int(request.form.get('annual_income', 500000)),
            'Health_Insurance': 1 if request.form.get('health_insurance') else 0
        }
        
        # Create DataFrame (required for the sklearn pipeline) - NO Patient_ID
        X = pd.DataFrame([patient_data])
        
        # Check if model is loaded
        if model is None:
            print("⚠️  No ML model available, using rule-based prediction")
            # Rule-based prediction system
            risk_score = calculate_rule_based_risk(patient_data)
            risk_category = 'Low' if risk_score < 0.33 else ('Medium' if risk_score < 0.66 else 'High')
            
            # Create feature importance for rule-based system
            feature_importance = [
                ('Age', f"{patient_data['Age']} years"),
                ('High Risk Conditions', f"{'High' if (patient_data['Diabetes'] + patient_data['Hypertension'] + patient_data['Obesity']) >= 2 else 'Low'}"),
                ('Lifestyle Factors', f"{'Poor' if (patient_data['Smoking'] + patient_data['Physical_Activity']) >= 1 else 'Good'}"),
                ('Blood Pressure', f"{patient_data['Systolic_BP']}/{patient_data['Diastolic_BP']} mmHg"),
                ('Cholesterol', f"{patient_data['Cholesterol_Level']} mg/dL"),
                ('Family History', 'Yes' if patient_data['Family_History'] else 'No'),
                ('Stress Level', f"{patient_data['Stress_Level']}/10")
            ]
            
            return render_template('result.html',
                                 risk_score=int(risk_score * 100),
                                 risk_category=risk_category,
                                 feature_importance=feature_importance)
        
        try:
            # Handle different model types
            global model_type
            if model_type == "simple":
                # Simple model expects only 12 features in specific order
                simple_features = [
                    patient_data['Age'],
                    patient_data['Diabetes'], 
                    patient_data['Hypertension'],
                    patient_data['Obesity'],
                    patient_data['Smoking'],
                    patient_data['Physical_Activity'],
                    patient_data['Diet_Score'],
                    patient_data['Cholesterol_Level'],
                    patient_data['Systolic_BP'],
                    patient_data['Diastolic_BP'],
                    patient_data['Family_History'],
                    patient_data['Stress_Level']
                ]
                
                # Convert to numpy array for simple model
                X_simple = np.array([simple_features])
                pred_prob = model.predict_proba(X_simple)[0][1]
                pred_class = model.predict(X_simple)[0]
                print(f"🔮 Simple model prediction: {pred_prob:.4f}")
                
            else:
                # Complex model expects DataFrame with all features
                X = pd.DataFrame([patient_data])
                pred_prob = model.predict_proba(X)[0][1]
                pred_class = model.predict(X)[0]
                print(f"🔮 Complex model prediction: {pred_prob:.4f}")
            
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
