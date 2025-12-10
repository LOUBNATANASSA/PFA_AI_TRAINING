"""
Disease Prediction ML Model Training Script
Trains a Random Forest classifier to predict diseases based on symptoms.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_and_preprocess_data():
    """Load the disease symptoms dataset and preprocess it."""
    # Load the dataset
    df = pd.read_csv(os.path.join(SCRIPT_DIR, 'DiseaseAndSymptoms.csv'))
    
    # Get all symptom columns
    symptom_columns = [col for col in df.columns if col.startswith('Symptom')]
    
    # Collect all unique symptoms
    all_symptoms = set()
    for col in symptom_columns:
        symptoms = df[col].dropna().str.strip().unique()
        all_symptoms.update(symptoms)
    
    # Remove empty strings
    all_symptoms.discard('')
    all_symptoms = sorted(list(all_symptoms))
    
    print(f"Found {len(all_symptoms)} unique symptoms")
    print(f"Found {df['Disease'].nunique()} unique diseases")
    
    return df, symptom_columns, all_symptoms

def create_feature_matrix(df, symptom_columns, all_symptoms):
    """Create binary feature matrix for symptoms."""
    # Create a dictionary for faster lookup
    symptom_to_idx = {symptom: idx for idx, symptom in enumerate(all_symptoms)}
    
    # Create feature matrix
    X = np.zeros((len(df), len(all_symptoms)), dtype=int)
    
    for row_idx, row in df.iterrows():
        for col in symptom_columns:
            symptom = row[col]
            if pd.notna(symptom):
                symptom = symptom.strip()
                if symptom in symptom_to_idx:
                    X[row_idx, symptom_to_idx[symptom]] = 1
    
    return X

def load_precautions():
    """Load disease precautions from CSV."""
    precautions_df = pd.read_csv(os.path.join(SCRIPT_DIR, 'Disease precaution.csv'))
    
    precautions_dict = {}
    for _, row in precautions_df.iterrows():
        disease = row['Disease'].strip() if pd.notna(row['Disease']) else None
        if disease:
            precs = []
            for i in range(1, 5):
                col = f'Precaution_{i}'
                if col in row and pd.notna(row[col]):
                    precs.append(row[col].strip())
            precautions_dict[disease] = precs
    
    return precautions_dict

def train_model():
    """Train the disease prediction model."""
    print("=" * 50)
    print("Disease Prediction Model Training")
    print("=" * 50)
    
    # Load and preprocess data
    print("\n1. Loading data...")
    df, symptom_columns, all_symptoms = load_and_preprocess_data()
    
    # Create feature matrix
    print("\n2. Creating feature matrix...")
    X = create_feature_matrix(df, symptom_columns, all_symptoms)
    
    # Encode disease labels
    print("\n3. Encoding labels...")
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df['Disease'].str.strip())
    
    # Split data
    print("\n4. Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train Random Forest
    print("\n5. Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    print("\n6. Evaluating model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nTest Accuracy: {accuracy * 100:.2f}%")
    
    # Load precautions
    print("\n7. Loading precautions...")
    precautions = load_precautions()
    
    # Save everything
    print("\n8. Saving model and data...")
    
    # Save model
    joblib.dump(model, os.path.join(SCRIPT_DIR, 'symptom_model.pkl'))
    
    # Save label encoder
    joblib.dump(label_encoder, os.path.join(SCRIPT_DIR, 'label_encoder.pkl'))
    
    # Save symptom list
    joblib.dump(all_symptoms, os.path.join(SCRIPT_DIR, 'symptom_list.pkl'))
    
    # Save precautions
    joblib.dump(precautions, os.path.join(SCRIPT_DIR, 'precautions.pkl'))
    
    print("\n" + "=" * 50)
    print("Training Complete!")
    print("=" * 50)
    print(f"\nFiles saved:")
    print(f"  - symptom_model.pkl")
    print(f"  - label_encoder.pkl")
    print(f"  - symptom_list.pkl")
    print(f"  - precautions.pkl")
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    print(f"Total Symptoms: {len(all_symptoms)}")
    print(f"Total Diseases: {len(label_encoder.classes_)}")
    
    return model, label_encoder, all_symptoms, precautions

if __name__ == "__main__":
    train_model()
