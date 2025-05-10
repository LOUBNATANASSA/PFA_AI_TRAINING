from django.shortcuts import render, HttpResponse , redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    
    return render(request,'welcome/home.html',{'title':'GeneGuard'})
    
def test_guidelines(request):
    return render(request,'welcome/test_guidelines.html',{'title':'GeneGuard'})

def test_finish(request):
    return render(request,'welcome/test_finish.html',{'title':'GeneGuard'})


def formulaire_Sickle_cell_anemia(request):
    return render(request,'welcome/Sickle_cell_anemia_form.html',{'title':'Formulaire'})

def formulaire_Galactosemia(request):
    return render(request,'welcome/Galactosemia_form.html',{'title':'Formulaire'})


def formulaire(request):
    return render(request,'welcome/formulaire.html',{'title':'Formulaire'})


def resultat(request):
    return render(request,'welcome/resultat.html',{'title':'Resultat'})

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
# views.py
from django.contrib.auth import  login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige vers la page d'accueil ou une autre
        else:
            return render(request, 'welcome/home.html')
    return render(request, 'welcome/login.html')
    
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile
from django.db import IntegrityError

def register_view(request): 
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        age = request.POST["age"]
        weight = request.POST["weight"]
        height = request.POST["height"]
        gender = request.POST["gender"]
        blood_type = request.POST["blood_type"]

        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            return render(request, "welcome/register.html", {
                "error": "Username already exists."
            })

        if User.objects.filter(email=email).exists():
            return render(request, "welcome/register.html", {
                "error": "Email already registered."
            })

        try:
            # Créer l'utilisateur
            user = User.objects.create_user(username=username, email=email, password=password)

            # Créer le profil associé
            UserProfile.objects.create(
                user=user,
                age=age,
                weight=weight,
                height=height,
                gender=gender,
                blood_type=blood_type
            )

            return redirect("login")

        except IntegrityError:
            return render(request, "welcome/register.html", {
                "error": "A problem occurred. Please try again."
            })

    return render(request, "welcome/register.html")


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect("login")

def historique_view(request):
    return render(request, "welcome/historique.html")