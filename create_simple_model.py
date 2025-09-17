#!/usr/bin/env python3
"""
Create a simple, Railway-compatible heart disease prediction model
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import sys

print("🔬 Creating Railway-Compatible Heart Disease Model...")
print(f"Python version: {sys.version}")

try:
    import sklearn
    print(f"scikit-learn version: {sklearn.__version__}")
except:
    print("❌ scikit-learn not available")

# Load dataset
print("\n📊 Loading dataset...")
df = pd.read_csv('heart.csv')
print(f"Dataset shape: {df.shape}")

# Simple preprocessing - use only numeric features and basic encoding
print("\n⚙️ Simple preprocessing...")

# Select most important features (avoiding complex pipelines)
important_features = [
    'Age', 'Diabetes', 'Hypertension', 'Obesity', 'Smoking', 
    'Physical_Activity', 'Diet_Score', 'Cholesterol_Level', 
    'Systolic_BP', 'Diastolic_BP', 'Family_History', 'Stress_Level'
]

# Create feature matrix with only numeric features
X_simple = df[important_features].copy()

# Target variable
y = df['Heart_Attack_Risk']

print(f"Selected features: {important_features}")
print(f"Feature matrix shape: {X_simple.shape}")
print(f"Target shape: {y.shape}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_simple, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")

# Train a simple Random Forest (no complex pipelines)
print("\n🚀 Training simple Random Forest...")
simple_model = RandomForestClassifier(
    n_estimators=100, 
    random_state=42, 
    class_weight='balanced'
)

simple_model.fit(X_train, y_train)

# Test the model
from sklearn.metrics import roc_auc_score
y_prob = simple_model.predict_proba(X_test)[:,1]
score = roc_auc_score(y_test, y_prob)

print(f"✅ Model trained successfully!")
print(f"ROC AUC Score: {score:.4f}")

# Save the simple model
print("\n💾 Saving simple model...")
joblib.dump(simple_model, "simple_heart_model.pkl")
print("✅ Simple model saved as simple_heart_model.pkl")

# Save feature list for the web app
feature_info = {
    'features': important_features,
    'model_type': 'simple_random_forest'
}
import json
with open('model_features.json', 'w') as f:
    json.dump(feature_info, f)

# Test the saved model
print("\n🧪 Testing saved simple model...")
loaded_model = joblib.load("simple_heart_model.pkl")

# Test with high-risk sample
test_sample = np.array([[55, 1, 1, 1, 1, 1, 3, 280, 160, 100, 1, 8]])  # High risk profile
prediction = loaded_model.predict(test_sample)
probability = loaded_model.predict_proba(test_sample)
risk_score = probability[0][1] * 100

print(f"✅ Test prediction successful!")
print(f"High-risk sample prediction: {prediction[0]}")
print(f"Risk probability: {probability[0][1]:.4f}")
print(f"Risk score: {risk_score:.1f}%")

# Test with low-risk sample
test_sample_low = np.array([[25, 0, 0, 0, 0, 4, 8, 180, 110, 70, 0, 3]])  # Low risk profile
prediction_low = loaded_model.predict(test_sample_low)
probability_low = loaded_model.predict_proba(test_sample_low)
risk_score_low = probability_low[0][1] * 100

print(f"Low-risk sample prediction: {prediction_low[0]}")
print(f"Risk probability: {probability_low[0][1]:.4f}")
print(f"Risk score: {risk_score_low:.1f}%")

print("\n🏁 Simple model creation completed!")
print(f"Model works with basic numpy arrays - no complex preprocessing needed!")