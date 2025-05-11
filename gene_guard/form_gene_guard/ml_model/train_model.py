import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# === Charger le fichier Excel ===
file_path = "diabetes.csv"

if not os.path.exists(file_path):
    print(f"❌ Le fichier '{file_path}' est introuvable.")
    exit()

try:
   df = pd.read_csv("diabetes.csv") 
   df.columns = df.columns.str.strip()
except Exception as e:
    print("❌ Erreur lors du chargement du fichier :", e)
    exit()

# === Nettoyage des noms de colonnes ===
df.columns = df.columns.str.strip()

print("📋 Colonnes du dataset :", list(df.columns))
print("🧪 Aperçu des premières lignes :\n", df.head())

# === Vérification présence de la colonne 'Outcome' ===
if 'Outcome' not in df.columns:
    print("❌ La colonne 'Outcome' est introuvable.")
    exit()

# === Séparation des données ===
X = df.drop(columns=['Outcome'])
y = df['Outcome']

# === Séparation en train/test ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === Entraînement du modèle ===
model = RandomForestClassifier()
model.fit(X_train, y_train)

# === Sauvegarde du modèle ===
model_file = "diabetes_model.pkl"
joblib.dump(model, model_file)

print(f"✅ Modèle entraîné et enregistré sous : {model_file}")
