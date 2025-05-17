from django.urls import path
from . import views
from .views import save_sickle_cell_result 
from .views import login_view,register_view ,logout_view ,historique_view
urlpatterns = [
    path('', views.home,name='home'),
    path('Formulaire/guidelines/', views.test_guidelines,name='guidelines'),
    path('Formulaire/complete/', views.test_finish,name='test_complete'),
    path('Formulaire/complete_hypercholesterolemia/', views.test_finish1,name='test_complete_hypercholesterolemia'),
    path('Formulaire/edit/', views.test_finish,name='edit_answers'),
    path('Formulaire/', views.formulaire,name='formulaire'),
    path('Formulaire/Sickle-cell-anemia', views.formulaire_Sickle_cell_anemia,name='formulaire_Sickle_cell_anemia'),
    path('Formulaire/Galactosemia', views.formulaire_Galactosemia,name='formulaire_Galactosemia'),
    path('Formulaire/hypercholesterolemia', views.formulaire_hypercholesterolemia,name='formulaire_hypercholesterolemia'),
    path('Resultat/', views.resultat,name='resultat'),
    path('Resultat_hypercholesterolemia/', views.resultat_hypercholesterolemia,name='resultat_hypercholesterolemia'),
    path('ListeMaladie/', views.ListeMaladie,name='ListeMaladie'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name="register"),
    path('logout/', logout_view, name='logout'),
    path('historique/', historique_view, name='historique'),

    path('save-result/', save_sickle_cell_result, name='save_sickle_cell_result'),

    path('get-sickle-cell-results/', views.get_sickle_cell_results, name='get_sickle_cell_results'),

 
    path('Cholesterol-results/', views.Cholesterol_results, name='Cholesterol_results'),  # Enregistrer les résultats
    path('get-cholesterol-results/', views.get_cholesterol_results, name='get_cholesterol_results'),  # Récupérer les résultats
    path('Formulaire/diabetes/', views.formulaire_diabetes, name='formulaire_diabetes'),
    path('predict-diabetes/', views.predict_diabetes_result, name='predict_diabetes_result'),
    path('Resultat/diabete/', views.resultat_diabete, name='resultat_diabete'),
    path('wiki/', views.wiki, name='wiki'),
    

]