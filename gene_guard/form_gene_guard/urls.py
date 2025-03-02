from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('Formulaire/', views.formulaire,name='formulaire'),
    path('Rseultat/', views.resultat,name='resultat'),

]