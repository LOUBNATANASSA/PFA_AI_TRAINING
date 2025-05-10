from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    gender = models.CharField(max_length=10)
    blood_type = models.CharField(max_length=3)

    def __str__(self):
        return self.user.username


class SickleCellResult(models.Model):
    user_id = models.AutoField(primary_key=True)          # PK auto-incrémentée

    # ► choix 1 : référence directe (UserProfile est déjà défini plus haut)
    user_profile = models.ForeignKey(
        UserProfile,
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
