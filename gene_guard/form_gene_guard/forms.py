# Fichier: gene_guard/form_gene_guard/forms.py
from django import forms

class StrokeForm(forms.Form):
    # --- Infos Personnelles ---
    gender = forms.ChoiceField(
        label="Sexe",
        choices=[('Male', 'Homme'), ('Female', 'Femme')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    age = forms.FloatField(
        label="Âge",
        min_value=1, max_value=120,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 65'})
    )

    # --- Données Médicales ---
    # Pour l'IA, on a besoin de 0 ou 1, c'est géré ici par les clés (0, 'Non')
    hypertension = forms.ChoiceField(
        label="Faites-vous de l'hypertension ?",
        choices=[(0, 'Non'), (1, 'Oui')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    heart_disease = forms.ChoiceField(
        label="Avez-vous une maladie cardiaque ?",
        choices=[(0, 'Non'), (1, 'Oui')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    avg_glucose_level = forms.FloatField(
        label="Niveau moyen de glucose (mg/dL)",
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 105.5'})
    )

    bmi = forms.FloatField(
        label="IMC (Indice de Masse Corporelle)",
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 28.4'})
    )

    # --- Situation ---
    ever_married = forms.ChoiceField(
        label="Êtes-vous marié(e) ou l'avez-vous été ?",
        choices=[('Yes', 'Oui'), ('No', 'Non')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    work_type = forms.ChoiceField(
        label="Type de travail",
        choices=[
            ('Private', 'Secteur Privé'),
            ('Self-employed', 'Indépendant'),
            ('Govt_job', 'Fonctionnaire'),
            ('children', 'Enfant / Étudiant'),
            ('Never_worked', 'Jamais travaillé')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    Residence_type = forms.ChoiceField(
        label="Zone de résidence",
        choices=[('Urban', 'Urbaine'), ('Rural', 'Rurale')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    smoking_status = forms.ChoiceField(
        label="Statut tabagique",
        choices=[
            ('formerly smoked', 'Ancien fumeur'),
            ('never smoked', 'Jamais fumé'),
            ('smokes', 'Fumeur actuel'),
            ('Unknown', 'Inconnu')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )