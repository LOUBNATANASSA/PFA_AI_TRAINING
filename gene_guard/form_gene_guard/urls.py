from django.urls import path
from . import views
from .views import save_sickle_cell_result 

urlpatterns = [
    path('', views.home,name='home'),
    path('Formulaire/guidelines/', views.test_guidelines,name='guidelines'),
    path('Formulaire/complete/', views.test_finish,name='test_complete'),
    path('Formulaire/edit/', views.test_finish,name='edit_answers'),
    path('Formulaire/', views.formulaire,name='formulaire'),
    path('Formulaire/Sickle-cell-anemia', views.formulaire_Sickle_cell_anemia,name='formulaire_Sickle_cell_anemia'),
    path('Formulaire/Galactosemia', views.formulaire_Galactosemia,name='formulaire_Galactosemia'),
    path('Formulaire/hypercholesterolemia', views.formulaire_Galactosemia,name='formulaire_hypercholesterolemia'),
    path('Resultat/', views.resultat,name='resultat'),
    path('ListeMaladie/', views.ListeMaladie,name='ListeMaladie'),
  


    path('save-result/', save_sickle_cell_result, name='save_sickle_cell_result'),

    path('get-sickle-cell-results/', views.get_sickle_cell_results, name='get_sickle_cell_results'),

    path('Formulaire/diabetes/', views.formulaire_diabetes, name='formulaire_diabetes'),
    path('predict-diabetes/', views.predict_diabetes_result, name='predict_diabetes_result'),
    path('Resultat/diabete/', views.resultat_diabete, name='resultat_diabete'),
    path('wiki/', views.wiki, name='wiki'),

    

]