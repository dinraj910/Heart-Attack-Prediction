#!/usr/bin/env python3
"""
Test script to verify the model loads and works correctly
"""
import os
import sys
import joblib
import numpy as np

print("🧪 Testing Model Loading and Prediction...")
print(f"Current working directory: {os.getcwd()}")
print(f"Python version: {sys.version}")

# Test model loading
model = None
try:
    possible_paths = [
        'models/heart_disease_pipeline.pkl',
        './models/heart_disease_pipeline.pkl',
        os.path.join('models', 'heart_disease_pipeline.pkl'),
        os.path.join(os.path.dirname(__file__), 'models', 'heart_disease_pipeline.pkl')
    ]
    
    for i, path in enumerate(possible_paths):
        print(f"Path {i+1}: {path} - {'EXISTS' if os.path.exists(path) else 'NOT FOUND'}")
        if os.path.exists(path):
            try:
                model = joblib.load(path)
                print(f"✅ Model loaded successfully from: {path}")
                print(f"Model type: {type(model)}")
                break
            except Exception as e:
                print(f"❌ Failed to load from {path}: {e}")
    
    if model is None:
        print("❌ No model could be loaded!")
        sys.exit(1)
    
    # Test prediction with sample data (including Patient_ID as expected by the model)
    print("\n🔮 Testing Prediction...")
    
    # Sample input data matching the dataset structure (including Patient_ID as the model expects it)
    sample_data_dict = {
        'Patient_ID': 1,  # The model expects this column
        'State_Name': 'Delhi',
        'Age': 45,
        'Gender': 'Male',
        'Diabetes': 0,
        'Hypertension': 0,
        'Obesity': 1,
        'Smoking': 0,
        'Alcohol_Consumption': 0,
        'Physical_Activity': 2,
        'Diet_Score': 7,
        'Cholesterol_Level': 220,
        'Triglyceride_Level': 180,
        'LDL_Level': 130,
        'HDL_Level': 45,
        'Systolic_BP': 140,
        'Diastolic_BP': 90,
        'Air_Pollution_Exposure': 1,
        'Family_History': 1,
        'Stress_Level': 6,
        'Healthcare_Access': 1,
        'Heart_Attack_History': 0,
        'Emergency_Response_Time': 200,
        'Annual_Income': 600000,
        'Health_Insurance': 1
    }
    
    # Convert to DataFrame (required for sklearn pipeline)
    import pandas as pd
    sample_df = pd.DataFrame([sample_data_dict])
    print(f"Sample data shape: {sample_df.shape}")
    print(f"Total features: {len(sample_df.columns)}")
    
    try:
        prediction = model.predict(sample_df)
        probability = model.predict_proba(sample_df)
        
        print(f"✅ Prediction successful!")
        print(f"Prediction: {prediction}")
        print(f"Probability: {probability}")
        print(f"Risk score: {probability[0][1] * 100:.1f}%")
        
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        import traceback
        traceback.print_exc()
        
except Exception as e:
    print(f"❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()

print("\n🏁 Test completed!")