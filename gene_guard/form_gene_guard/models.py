from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    age = models.PositiveIntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    gender = models.CharField(max_length=10)
    blood_type = models.CharField(max_length=3)

    def __str__(self):
        return self.user.username

#hadi dyal Cholesterol

from django.db import models

class CholesterolResult(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_profile_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    responses = models.JSONField()  # Stocke les réponses en tant que dictionnaire JSON
    created_at = models.DateTimeField(auto_now_add=True)  # Date d'enregistrement

    def __str__(self):
        return f"Result ID: {self.user_id}"

class SickleCellResult(models.Model):
    user_id = models.AutoField(primary_key=True)          # PK auto-incrémentée

    # ► choix 1 : référence directe (UserProfile est déjà défini plus haut)
    user_profile = models.ForeignKey(
        UserProfile,
        null=True,
        on_delete=models.CASCADE,
        related_name="sickle_results"
    )

    # ► si tu mets la classe en dessous : 'form_gene_guard.UserProfile'
    # user_profile = models.ForeignKey(
    #     'form_gene_guard.UserProfile',
    #     on_delete=models.CASCADE,
    #     related_name="sickle_results"
    # )

    responses = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result #{self.user_id}"

class GalactosemiaResult(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    responses = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Galactosemia Result #{self.user_id}"

class DiabetesResult(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    # Store input data (pregnancies, glucose, etc.)
    input_data = models.JSONField()
    # Store result (Probability %, Risk Level)
    result_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diabetes Result #{self.user_id}"

class CardioResult(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    input_data = models.JSONField()
    result_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cardio Result #{self.user_id}"

class GeneralResult(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    selected_symptoms = models.JSONField()
    predicted_diseases = models.JSONField() # Top 5 predictions
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"General Result #{self.user_id}"