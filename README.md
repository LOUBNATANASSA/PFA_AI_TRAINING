
# 🧬 GeneGuard

**GeneGuard** est une application web développée avec **Django** permettant l’analyse, la prédiction et la gestion des données génétiques. Le projet intègre des algorithmes de Machine Learning pour offrir des prédictions personnalisées.

---

## 📌 Fonctionnalités principales

- 🔐 Authentification utilisateur
- 📂 Upload et gestion de données médicales
- 🧠 Prédiction basée sur un modèle Machine Learning (chargé via `joblib`)
- 📊 Interface utilisateur intuitive pour visualiser les résultats
- 📁 Base de données SQLite intégrée

---

## ⚙️ Technologies utilisées

| Outil / Framework    | Description                          |
|----------------------|--------------------------------------|
| Django               | Framework web backend                |
| SQLite               | Base de données légère intégrée      |
| scikit-learn (`sklearn`) | Librairie de Machine Learning       |
| NumPy                | Calcul scientifique                  |
| Joblib               | Sérialisation et chargement de modèles ML |

---

## 🚀 Installation et lancement

1. **Cloner le projet**
```bash
git clone https://github.com/tahabenhima/GeneGuard.git
cd GeneGuard

2. **Créer un environnement virtuel (optionnel mais recommandé)**

python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Mac/Linux

3. **Installer les dépendances**

pip install -r requirements.txt

4. **Lancer le serveur**
Lancer le serveur

5. **Ouvrir dans le navigateur **
http://127.0.0.1:8000/

