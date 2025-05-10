from django.contrib import admin


from .models import SickleCellResult  # Import du modèle

admin.site.register(SickleCellResult)  # Enregistrement dans l'admin

from .models import CholesterolResult  # Import du modèle

admin.site.register(CholesterolResult)  
