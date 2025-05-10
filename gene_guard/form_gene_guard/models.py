from django.db import models





# hadi pour la base de donnees
class SickleCellResult(models.Model):
    user_id = models.AutoField(primary_key=True)  # ID unique
    responses = models.JSONField()  # Stocke les réponses sous forme JSON
    created_at = models.DateTimeField(auto_now_add=True)  # Date d'enregistrement

    def __str__(self):
        return f"Result ID: {self.user_id}"

#hadi dyal Cholesterol

from django.db import models

class CholesterolResult(models.Model):
    user_id = models.AutoField(primary_key=True)
    responses = models.JSONField()  # Stocke les réponses en tant que dictionnaire JSON
    created_at = models.DateTimeField(auto_now_add=True)  # Date d'enregistrement

    def __str__(self):
        return f"Result ID: {self.user_id}"
