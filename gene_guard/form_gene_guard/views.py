from django.shortcuts import render, HttpResponse , redirect

# Create your views here.
def home(request):
    
    return render(request,'welcome/home.html',{'title':'GeneGuard'})
    
def test_guidelines(request):
    return render(request,'welcome/test_guidelines.html',{'title':'GeneGuard'})

def test_finish(request):
    return render(request,'welcome/test_finish.html',{'title':'GeneGuard'})

def test_finish1(request):
    return render(request,'welcome/test_finish1.html',{'title':'GeneGuard'})


def formulaire_Sickle_cell_anemia(request):
    return render(request,'welcome/Sickle_cell_anemia_form.html',{'title':'Formulaire'})

def formulaire_Galactosemia(request):
    return render(request,'welcome/Galactosemia_form.html',{'title':'Formulaire'})


def formulaire(request):
    return render(request,'welcome/formulaire.html',{'title':'Formulaire'})

def formulaire_hypercholesterolemia(request):
    return render(request,'welcome/hypercholesterolemia.html',{'title':'Formulaire'})

def resultat(request):
    return render(request,'welcome/resultat.html',{'title':'Resultat'})

def resultat_hypercholesterolemia(request):
    return render(request,'welcome/resultat_hypercholesterolemia.html',{'title':'Resultat_hypercholesterolemia'})

def ListeMaladie(request):
    return render(request,'welcome/ListeMaladie.html',{'title':'ListeMaladie'})



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SickleCellResult  # Import du modèle

@csrf_exempt  # Désactive la protection CSRF (utile pour le développement)
def save_sickle_cell_result(request):
    if request.method == "POST":  # Vérifie si la requête est POST
        try:
            data = json.loads(request.body)  # Convertit le JSON reçu en dictionnaire Python
            result = SickleCellResult.objects.create(responses=data)  # Enregistre en base
            return JsonResponse({"message": "Données enregistrées avec succès", "id": result.user_id}, status=201)  
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)  # En cas d'erreur
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)  # Si ce n'est pas une requête POST





def get_sickle_cell_results(request):
    # Récupérer le dernier enregistrement
    result = SickleCellResult.objects.last()  # Récupère le dernier enregistrement
    
    if result:
        # Si un résultat existe, retourner les réponses sous forme de JSON
        return JsonResponse(result.responses, safe=False)
    else:
        # Si aucun résultat n'est trouvé, renvoyer une erreur
        return JsonResponse({"error": "Aucun résultat trouvé."}, status=404)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CholesterolResult

@csrf_exempt  # Pour autoriser la requête POST
def Cholesterol_results(request):
    if request.method == 'POST':
        try:
            # Récupérer les données JSON envoyées par le frontend
            data = json.loads(request.body)
            responses = data.get('responses', {})
            
            # Créer un nouvel objet CholesterolResult avec les réponses
            result = CholesterolResult(responses=responses)
            result.save()  # Sauvegarder dans la base de données
            
            # Répondre avec un message de succès
            return JsonResponse({'status': 'success', 'message': 'Résultats enregistrés avec succès'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Données invalides'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Méthode HTTP non autorisée'}, status=405)


from django.http import JsonResponse
from .models import CholesterolResult

def get_cholesterol_results(request):
    try:
        # Récupérer tous les résultats de cholestérol dans la base de données
        results = CholesterolResult.objects.all().values('user_id', 'responses', 'created_at')
        
        # Retourner les résultats sous forme de JSON
        return JsonResponse({'status': 'success', 'results': list(results)}, safe=False)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

