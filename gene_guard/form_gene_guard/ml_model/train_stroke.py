# Fichier: ml_model/train_stroke.py
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

# recuperer le chemi du dossier actuel
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2.construire chemin vers la dataset
csv_path = os.path.join(current_dir, 'stroke.csv')

print(f"Chargement des données depuis : {csv_path}")

try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    print("ERREUR : Je ne trouve pas 'stroke.csv'. Avez-vous bien renommé le fichier ?")
    exit()

# preparer les donnees
X = df.drop(['stroke', 'id'], axis=1)
y = df['stroke']

# separation des colonnes
numeric_features = ['age', 'avg_glucose_level', 'bmi']
categorical_features = ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']
passthrough_features = ['hypertension', 'heart_disease']

# 4. Pipelines de nettoyage
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features),
        ('pass', 'passthrough', passthrough_features)])

# 5. Création du Modèle
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42))
])

# 6. Entraînement
print("Entraînement en cours...")
model.fit(X, y)

# 7. Sauvegarde du modèle (stroke_model.pkl) dans le même dossier
output_path = os.path.join(current_dir, 'stroke_model.pkl')
joblib.dump(model, output_path)

print(f"SUCCÈS ! Modèle sauvegardé ici : {output_path}")