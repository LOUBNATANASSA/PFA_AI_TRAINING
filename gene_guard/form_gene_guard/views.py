from django.shortcuts import render, HttpResponse , redirect
from django.contrib.auth import authenticate, login, logout
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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

def formulaire_diabetes(request):
    return render(request, 'welcome/resultat-diabetes.html', {'title': 'Évaluation Diabète'})
def resultat_diabete(request):
    result_raw = request.session.get('diabetes_result', '')
    parts = result_raw.split("Probabilité estimée : ")
    conseil = parts[0] if len(parts) > 0 else ""
    pourcentage_str = parts[1].replace(" %", "") if len(parts) > 1 else "0"
    
    try:
        pourcentage = float(pourcentage_str)
    except:
        pourcentage = 0

    return render(request, 'welcome/resultat_diabete.html', {
        'conseil': conseil.strip(),
        'pourcentage': pourcentage
    })

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
    if request.method != "GET":
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)
    try:
        results = CholesterolResult.objects.all().values('user_id', 'responses', 'created_at')
        return JsonResponse({'status': 'success', 'results': list(results)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
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
#model training
@csrf_exempt
def predict_diabetes_result(request):
    if request.method == 'POST':
        try:
            data = request.POST
            features = [
                float(data.get("Pregnancies")),
                float(data.get("Glucose")),
                float(data.get("BloodPressure")),
                float(data.get("SkinThickness")),
                float(data.get("Insulin")),
                float(data.get("BMI")),
                float(data.get("DiabetesPedigreeFunction")),
                float(data.get("Age")),
            ]
            model_path = os.path.join(os.path.dirname(__file__), 'ml_model', 'diabetes_model.pkl')
            model = joblib.load(model_path)

            probability = model.predict_proba([features])[0][1]
            percentage = round(probability * 100, 2)
            result_text = "⚠️ High risk of diabetes" if percentage >= 50 else "✅ Low risk of diabetes"
            full_result = f"{result_text} Probabilité estimée : {percentage} %"

            # Stocker le résultat dans la session
            request.session['diabetes_result'] = full_result
            return JsonResponse({"redirect_url": "/Resultat/diabete/"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)


#wiki 
def wiki(request):
    diseases = [
    {
        "name": "Sickle Cell Anemia",
        "description": "A genetic blood disorder that causes red blood cells to become misshapen and break down.",
        "symptoms": ["Fatigue", "Pain episodes", "Swelling", "Frequent infections"],
        "causes": "Inherited when both parents carry the sickle cell gene.",
        "treatment": "Pain management, blood transfusions, bone marrow transplant."
    },
    {
        "name": "Cystic Fibrosis",
        "description": "A hereditary disease that affects the lungs and digestive system, causing thick mucus buildup.",
        "symptoms": ["Chronic cough", "Frequent lung infections", "Poor weight gain", "Shortness of breath"],
        "causes": "Mutation in the CFTR gene.",
        "treatment": "Chest physiotherapy, enzyme supplements, antibiotics, lung transplant."
    },
    {
        "name": "Hemophilia",
        "description": "A disorder in which blood doesn’t clot normally due to lack of clotting factors.",
        "symptoms": ["Prolonged bleeding", "Easy bruising", "Joint pain"],
        "causes": "X-linked recessive gene mutation (mostly affects males).",
        "treatment": "Clotting factor replacement therapy."
    },
    {
        "name": "Huntington’s Disease",
        "description": "A progressive brain disorder that causes uncontrolled movements and cognitive decline.",
        "symptoms": ["Involuntary movements", "Mood changes", "Memory loss", "Difficulty speaking"],
        "causes": "Mutation in the HTT gene.",
        "treatment": "No cure, but medications and therapy can help manage symptoms."
    },
    {
        "name": "Tay-Sachs Disease",
        "description": "A rare genetic disorder that destroys nerve cells in the brain and spinal cord.",
        "symptoms": ["Loss of motor skills", "Seizures", "Vision and hearing loss"],
        "causes": "Mutation in the HEXA gene, common in Ashkenazi Jewish populations.",
        "treatment": "No cure, supportive care only."
    },
    {
        "name": "Thalassemia",
        "description": "A blood disorder involving less than normal amounts of an oxygen-carrying protein.",
        "symptoms": ["Fatigue", "Pale skin", "Delayed growth", "Enlarged spleen"],
        "causes": "Mutations in genes involved in hemoglobin production.",
        "treatment": "Regular blood transfusions, iron chelation therapy."
    },
    {
        "name": "Familial Hypercholesterolemia",
        "description": "An inherited condition causing very high cholesterol levels and early heart disease.",
        "symptoms": ["High LDL cholesterol", "Chest pain", "Xanthomas (fatty skin deposits)"],
        "causes": "Mutation in LDL receptor gene.",
        "treatment": "Statins, lifestyle changes, sometimes LDL apheresis."
    },
    {
        "name": "Albinism",
        "description": "A group of inherited disorders that reduce the amount of melanin in the skin, hair, and eyes.",
        "symptoms": ["Very light skin and hair", "Vision problems", "Increased sun sensitivity"],
        "causes": "Mutations in genes involved in melanin production.",
        "treatment": "Sun protection, vision support, regular skin monitoring."
    },
    {
        "name": "Polycystic Kidney Disease (PKD)",
        "description": "A genetic disorder that causes many cysts to grow in the kidneys.",
        "symptoms": ["Back or side pain", "High blood pressure", "Kidney failure"],
        "causes": "Mutations in PKD1 or PKD2 genes.",
        "treatment": "Blood pressure control, dialysis, kidney transplant."
    },
    {
        "name": "Marfan Syndrome",
        "description": "A genetic disorder that affects connective tissue, often impacting the heart, eyes, and skeleton.",
        "symptoms": ["Tall stature", "Long limbs", "Heart valve issues", "Flexible joints"],
        "causes": "Mutation in FBN1 gene (fibrillin-1).",
        "treatment": "Monitoring of heart/aorta, beta-blockers, surgery if needed."
    },
]

    return render(request, 'welcome/wiki.html', {'diseases': diseases})

# la maladie stroke
import os
import joblib
import pandas as pd
from django.shortcuts import render
from .forms import StrokeForm  # On importe notre nouveau formulaire

# --- Chargement du modèle ---
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'ml_model', 'stroke_model.pkl')

try:
    model = joblib.load(model_path)
    print("Modèle IA chargé.")
except FileNotFoundError:
    model = None
    print("ERREUR : Modèle IA introuvable.")

def prediction_view(request):
    resultat = None
    proba_display = None

    # Si l'utilisateur envoie le formulaire
    if request.method == 'POST':
        # Django remplit le formulaire avec les données reçues
        form = StrokeForm(request.POST)
        
        # Django vérifie si tout est correct (chiffres valides, etc.)
        if form.is_valid():
            # On récupère les données "propres" (nettoyées)
            data = form.cleaned_data
            
            # On prépare le DataFrame pour l'IA
            # Note : form.cleaned_data convertit déjà '0' en entier 0 si besoin
            input_df = pd.DataFrame([{
                'gender': data['gender'],
                'age': data['age'],
                'hypertension': int(data['hypertension']), # Sécurité pour forcer l'entier
                'heart_disease': int(data['heart_disease']),
                'ever_married': data['ever_married'],
                'work_type': data['work_type'],
                'Residence_type': data['Residence_type'],
                'avg_glucose_level': data['avg_glucose_level'],
                'bmi': data['bmi'],
                'smoking_status': data['smoking_status']
            }])

            if model:
                # Prédiction
                prediction = model.predict(input_df)[0]
                proba = model.predict_proba(input_df)[0][1]
                
                # Affichage
                proba_display = round(proba * 100, 2)
                if prediction == 1:
                    resultat = "RISQUE ÉLEVÉ"
                else:
                    resultat = "Faible Risque"
    else:
        # Si on arrive sur la page, on affiche un formulaire vide
        form = StrokeForm()

    return render(request, 'welcome/predict.html', {
        'form': form,
        'resultat': resultat,
        'proba': proba_display
    })