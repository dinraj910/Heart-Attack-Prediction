#!/usr/bin/env python3
"""
Retrain the heart disease model with Railway-compatible versions
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib
import sys

print("🔬 Retraining Heart Disease Model...")
print(f"Python version: {sys.version}")

# Check versions
try:
    import sklearn
    print(f"scikit-learn version: {sklearn.__version__}")
except:
    print("❌ scikit-learn not available")

# Load dataset
print("\n📊 Loading dataset...")
df = pd.read_csv('heart.csv')
print(f"Dataset shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

# Prepare features
X = df.drop(columns=['Patient_ID', 'Heart_Attack_Risk'])  # Exclude Patient_ID and target
y = df['Heart_Attack_Risk']

print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")

# Identify categorical vs numeric
cat_cols = X.select_dtypes(include=['object']).columns.tolist()
num_cols = X.select_dtypes(include=['int64','float64']).columns.tolist()

print(f"Categorical columns: {cat_cols}")
print(f"Numeric columns: {num_cols}")

# Create pipelines
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, num_cols),
        ('cat', categorical_transformer, cat_cols)
    ]
)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")

# Train models
print("\n🚀 Training models...")

# Logistic Regression
pipe_lr = Pipeline(steps=[('preprocessor', preprocessor),
                          ('clf', LogisticRegression(max_iter=1000, class_weight='balanced'))])

# Random Forest
pipe_rf = Pipeline(steps=[('preprocessor', preprocessor),
                          ('clf', RandomForestClassifier(n_estimators=200, class_weight='balanced', random_state=42))])

models = {"LogisticRegression": pipe_lr, "RandomForest": pipe_rf}
results = {}

for name, model in models.items():
    print(f"\n▶ Training {name}")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:,1]
    
    print(f"ROC AUC: {roc_auc_score(y_test, y_prob):.4f}")
    results[name] = (model, roc_auc_score(y_test, y_prob))

# Select best model
best_model_name = max(results.items(), key=lambda x: x[1][1])[0]
best_model = results[best_model_name][0]
best_score = results[best_model_name][1]

print(f"\n✅ Best model: {best_model_name} (ROC AUC: {best_score:.4f})")

# Save the model
print("\n💾 Saving model...")
joblib.dump(best_model, "heart_disease_pipeline.pkl")
print("✅ Model saved as heart_disease_pipeline.pkl")

# Test the saved model
print("\n🧪 Testing saved model...")
loaded_model = joblib.load("heart_disease_pipeline.pkl")

# Create sample data for testing
sample_data = {
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

sample_df = pd.DataFrame([sample_data])
print(f"Sample data shape: {sample_df.shape}")

try:
    prediction = loaded_model.predict(sample_df)
    probability = loaded_model.predict_proba(sample_df)
    risk_score = probability[0][1] * 100
    
    print(f"✅ Test prediction successful!")
    print(f"Prediction: {prediction[0]}")
    print(f"Risk probability: {probability[0][1]:.4f}")
    print(f"Risk score: {risk_score:.1f}%")
    
except Exception as e:
    print(f"❌ Test prediction failed: {e}")
    import traceback
    traceback.print_exc()

print("\n🏁 Model retraining completed!")