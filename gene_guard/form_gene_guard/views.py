from django.shortcuts import render, HttpResponse , redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
# Page d'accueil accessible à tous
def home(request):
    return render(request,'welcome/home.html',{'title':'GeneGuard'})

# ============================================================
# PAGES PROTÉGÉES - Nécessitent une connexion utilisateur
# ============================================================

@login_required
def ListeMaladie(request):
    return render(request,'welcome/ListeMaladie.html',{'title':'ListeMaladie'})

# ============================================================
# PAGES PROTÉGÉES - Nécessitent une connexion utilisateur
# ============================================================

@login_required
def test_guidelines(request):
    return render(request,'welcome/test_guidelines.html',{'title':'GeneGuard'})

@login_required
def test_finish(request):
    return render(request,'welcome/test_finish.html',{'title':'GeneGuard'})

@login_required
def test_finish1(request):
    return render(request,'welcome/test_finish1.html',{'title':'GeneGuard'})

@login_required
def formulaire_Sickle_cell_anemia(request):
    return render(request,'welcome/Sickle_cell_anemia_form.html',{'title':'Formulaire'})

@login_required
def formulaire_Galactosemia(request):
    return render(request,'welcome/Galactosemia_form.html',{'title':'Formulaire'})

@login_required
def formulaire(request):
    return render(request,'welcome/formulaire.html',{'title':'Formulaire'})

@login_required
def formulaire_hypercholesterolemia(request):
    return render(request,'welcome/hypercholesterolemia.html',{'title':'Formulaire'})

@login_required
def resultat(request):
    return render(request,'welcome/resultat.html',{'title':'Resultat'})

@login_required
def resultat_hypercholesterolemia(request):
    return render(request,'welcome/resultat_hypercholesterolemia.html',{'title':'Resultat_hypercholesterolemia'})

@login_required
def formulaire_diabetes(request):
    fields = [
        {"name": "Pregnancies", "label": "Pregnancies", "placeholder": "e.g., 2"},
        {"name": "Glucose", "label": "Glucose", "placeholder": "e.g., 120"},
        {"name": "BloodPressure", "label": "Blood Pressure", "placeholder": "e.g., 80"},
        {"name": "SkinThickness", "label": "Skin Thickness", "placeholder": "e.g., 20"},
        {"name": "Insulin", "label": "Insulin", "placeholder": "e.g., 85"},
        {"name": "BMI", "label": "BMI", "placeholder": "e.g., 25.5"},
        {"name": "DiabetesPedigreeFunction", "label": "Diabetes Pedigree Function", "placeholder": "e.g., 0.5"},
        {"name": "Age", "label": "Age", "placeholder": "e.g., 35"}
    ]
    return render(request, 'welcome/diabetes_form.html', {'title': 'Évaluation Diabète', 'fields': fields})

@login_required
def resultat_diabete(request):
    result_data = request.session.get('diabetes_result', {})
    
    if isinstance(result_data, str):
        # Fallback for old session data format
        parts = result_data.split("Probabilité estimée : ")
        conseil = parts[0] if len(parts) > 0 else ""
        pourcentage_str = parts[1].replace(" %", "") if len(parts) > 1 else "0"
        try:
            pourcentage = float(pourcentage_str)
        except:
            pourcentage = 0
        precautions = []
    else:
        conseil = result_data.get('result', '')
        pourcentage = result_data.get('percentage', 0)
        precautions = result_data.get('precautions', [])

    return render(request, 'welcome/resultat_diabete.html', {
        'conseil': conseil.strip(),
        'pourcentage': pourcentage,
        'precautions': precautions
    })

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SickleCellResult, UserProfile, GalactosemiaResult, DiabetesResult, CardioResult, GeneralResult # Import des modèles

@csrf_exempt
def save_sickle_cell_result(request):
    """Sauvegarde les résultats du test Sickle Cell - AJAX endpoint"""
    # LOGGING START
    import datetime
    with open('debug_log.txt', 'a') as f:
        f.write(f"\n--- [Sickle Save] Request at {datetime.datetime.now()} ---\n")
        f.write(f"User: {request.user} (Is Auth: {request.user.is_authenticated})\n")
        f.write(f"Method: {request.method}\n")
        f.write(f"Cookies: {request.COOKIES.keys()}\n")
    # LOGGING END

    # Vérification manuelle de l'authentification pour AJAX
    if not request.user.is_authenticated:
        with open('debug_log.txt', 'a') as f: f.write("Error: Not authenticated\n")
        return JsonResponse({"error": "Non authentifié", "redirect": "/login/"}, status=401)
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            with open('debug_log.txt', 'a') as f: f.write(f"Data received: {data}\n")
            
            # Récupérer le profil de l'utilisateur connecté
            user_profile = UserProfile.objects.get(user=request.user)
            with open('debug_log.txt', 'a') as f: f.write(f"Profile found: {user_profile.id}\n")
            
            # Créer le résultat lié à l'utilisateur
            result = SickleCellResult.objects.create(
                user_profile=user_profile,
                responses=data
            )
            with open('debug_log.txt', 'a') as f: f.write(f"SUCCESS: Saved Result ID {result.user_id}\n")
            return JsonResponse({"message": "Données enregistrées avec succès", "id": result.user_id}, status=201)
        except UserProfile.DoesNotExist:
            with open('debug_log.txt', 'a') as f: f.write("Error: UserProfile DoesNotExist\n")
            return JsonResponse({"error": "Profil utilisateur non trouvé. Veuillez compléter votre inscription."}, status=400)
        except Exception as e:
            with open('debug_log.txt', 'a') as f: f.write(f"Error: {e}\n")
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)





def get_sickle_cell_results(request):
    # Récupérer le dernier enregistrement
    result = SickleCellResult.objects.last()  # Récupère le dernier enregistrement
    
    if result:
        # Si un résultat existe, retourner les réponses sous forme de JSON
        return JsonResponse(result.responses, safe=False)
    else:
        # Si aucun résultat n'est trouvé, renvoyer une erreur
        return JsonResponse({"error": "Aucun résultat trouvé."}, status=404)

@csrf_exempt
def save_galactosemia_result(request):
    """Sauvegarde les résultats du test Galactosemia - AJAX endpoint"""
    # Vérification manuelle de l'authentification pour AJAX
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Non authentifié", "redirect": "/login/"}, status=401)
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # Récupérer le profil de l'utilisateur connecté
            user_profile = UserProfile.objects.get(user=request.user)
            # Créer le résultat lié à l'utilisateur
            result = GalactosemiaResult.objects.create(
                user_profile=user_profile,
                responses=data
            )
            return JsonResponse({"message": "Données enregistrées avec succès", "id": result.user_id}, status=201)
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "Profil utilisateur non trouvé. Veuillez compléter votre inscription."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CholesterolResult

@csrf_exempt
def Cholesterol_results(request):
    """Sauvegarde les résultats du test Cholestérol - AJAX endpoint"""
    # LOGGING START
    import datetime
    with open('debug_log.txt', 'a') as f:
        f.write(f"\n--- [Cholesterol Save] Request at {datetime.datetime.now()} ---\n")
        f.write(f"User: {request.user} (Is Auth: {request.user.is_authenticated})\n")
    # LOGGING END

    # Vérification manuelle de l'authentification pour AJAX
    if not request.user.is_authenticated:
        with open('debug_log.txt', 'a') as f: f.write("Error: Not authenticated\n")
        return JsonResponse({'status': 'error', 'message': 'Non authentifié', 'redirect': '/login/'}, status=401)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            with open('debug_log.txt', 'a') as f: f.write(f"Data received: {data}\n")
            responses = data.get('responses', {})
            
            # Récupérer le profil de l'utilisateur connecté
            user_profile = UserProfile.objects.get(user=request.user)
            with open('debug_log.txt', 'a') as f: f.write(f"Profile found: {user_profile.id}\n")
            
            # Créer le résultat lié à l'utilisateur
            result = CholesterolResult(
                user_profile_id=user_profile,
                responses=responses
            )
            result.save()
            with open('debug_log.txt', 'a') as f: f.write(f"SUCCESS: Saved Result ID {result.user_id}\n")
            return JsonResponse({'status': 'success', 'message': 'Résultats enregistrés avec succès'})
        except UserProfile.DoesNotExist:
            with open('debug_log.txt', 'a') as f: f.write("Error: UserProfile DoesNotExist\n")
            return JsonResponse({'status': 'error', 'message': 'Profil utilisateur non trouvé. Veuillez compléter votre inscription.'}, status=400)
        except json.JSONDecodeError:
            with open('debug_log.txt', 'a') as f: f.write("Error: JSON Decode Error\n")
            return JsonResponse({'status': 'error', 'message': 'Données invalides'}, status=400)
        except Exception as e:
            with open('debug_log.txt', 'a') as f: f.write(f"Error: {e}\n")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
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
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'welcome/login.html', {
                'error': 'Nom d\'utilisateur ou mot de passe incorrect.'
            })
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

@login_required
def profile_view(request):
    """Affiche le profil utilisateur avec ses informations et historique de tests"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        # Calculer l'IMC
        height_m = user_profile.height / 100
        imc = round(user_profile.weight / (height_m * height_m), 1) if height_m > 0 else 0
    except UserProfile.DoesNotExist:
        user_profile = None
        imc = 0
    
    # Récupérer l'historique des tests de l'utilisateur
    sickle_results = []
    cholesterol_results = []
    
    if user_profile:
        sickle_results = SickleCellResult.objects.filter(user_profile=user_profile).order_by('-created_at')
        cholesterol_results = CholesterolResult.objects.filter(user_profile_id=user_profile).order_by('-created_at')
    
    return render(request, "welcome/profile.html", {
        'user_profile': user_profile,
        'imc': imc,
        'sickle_results': sickle_results,
        'cholesterol_results': cholesterol_results,
    })

@login_required
def historique_view(request):
    """Affiche l'historique des tests de l'utilisateur"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    # Récupérer tous les résultats de tests
    sickle_results = []
    cholesterol_results = []
    galactosemia_results = []
    diabetes_results = []
    cardio_results = []
    general_results = []
    
    if user_profile:
        sickle_results = SickleCellResult.objects.filter(user_profile=user_profile).order_by('-created_at')
        cholesterol_results = CholesterolResult.objects.filter(user_profile_id=user_profile).order_by('-created_at')
        galactosemia_results = GalactosemiaResult.objects.filter(user_profile=user_profile).order_by('-created_at')
        diabetes_results = DiabetesResult.objects.filter(user_profile=user_profile).order_by('-created_at')
        cardio_results = CardioResult.objects.filter(user_profile=user_profile).order_by('-created_at')
        general_results = GeneralResult.objects.filter(user_profile=user_profile).order_by('-created_at')
    
    # Compter le nombre total de tests
    total_tests = len(sickle_results) + len(cholesterol_results) + len(galactosemia_results) + len(diabetes_results) + len(cardio_results) + len(general_results)
    
    return render(request, "welcome/historique.html", {
        'user_profile': user_profile,
        'sickle_results': sickle_results,
        'cholesterol_results': cholesterol_results,
        'galactosemia_results': galactosemia_results,
        'diabetes_results': diabetes_results,
        'cardio_results': cardio_results,
        'general_results': general_results,
        'total_tests': total_tests,
    })
#model training
@csrf_exempt
def predict_diabetes_result(request):
    if request.method == 'POST':
        try:
            data = request.POST
            # Extract features
            pregnancies = float(data.get("Pregnancies"))
            glucose = float(data.get("Glucose"))
            bp = float(data.get("BloodPressure"))
            skin = float(data.get("SkinThickness"))
            insulin = float(data.get("Insulin"))
            bmi = float(data.get("BMI"))
            dpf = float(data.get("DiabetesPedigreeFunction"))
            age = float(data.get("Age"))

            features = [pregnancies, glucose, bp, skin, insulin, bmi, dpf, age]
            
            model_path = os.path.join(os.path.dirname(__file__), 'ml_model', 'diabetes_model.pkl')
            model = joblib.load(model_path)

            probability = model.predict_proba([features])[0][1]
            percentage = round(probability * 100, 2)
            result_text = "⚠️ High risk of diabetes" if percentage >= 50 else "✅ Low risk of diabetes"
            
            # Generate Precautions
            precautions = []
            if percentage >= 50:
                precautions.append("Consult a healthcare provider for a comprehensive diabetes screening.")
                precautions.append("Monitor your blood sugar levels regularly.")
            
            if bmi >= 25:
                precautions.append("Your BMI indicates you may be overweight. Aim for a healthy weight through diet and exercise.")
            if glucose > 140:
                precautions.append("Your glucose levels are high. Reduce intake of sugary foods and refined carbs.")
            if bp > 80:
                precautions.append("Monitor your blood pressure. Reduce sodium intake and manage stress.")
            if age > 45:
                precautions.append("Age is a risk factor. Ensure you have regular annual check-ups.")
            if insulin > 100: # Arbitrary threshold for example
                 precautions.append("High insulin levels may indicate insulin resistance.")

            if not precautions:
                precautions.append("Maintain a healthy lifestyle with balanced diet and regular exercise.")

            # Store result in session as a dict
            request.session['diabetes_result'] = {
                'result': result_text,
                'percentage': percentage,
                'precautions': precautions
            }
            
            # SAUVEGARDER EN BASE DE DONNEES SI CONNECTÉ
            if request.user.is_authenticated:
                try:
                    user_profile = UserProfile.objects.get(user=request.user)
                    DiabetesResult.objects.create(
                        user_profile=user_profile,
                        input_data=data,
                        result_data={"result": result_text, "percentage": percentage, "precautions": precautions}
                    )
                except Exception as e:
                    print(f"Erreur sauvegarde diabetes: {e}")

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


# ===== GENERAL DISEASE PREDICTION FROM SYMPTOMS =====
import numpy as np

# Load symptom prediction model
symptom_model_dir = os.path.join(current_dir, 'ml_model')
try:
    symptom_model = joblib.load(os.path.join(symptom_model_dir, 'symptom_model.pkl'))
    label_encoder = joblib.load(os.path.join(symptom_model_dir, 'label_encoder.pkl'))
    symptom_list = joblib.load(os.path.join(symptom_model_dir, 'symptom_list.pkl'))
    precautions_dict = joblib.load(os.path.join(symptom_model_dir, 'precautions.pkl'))
    print("Symptom prediction model loaded successfully.")
except FileNotFoundError as e:
    symptom_model = None
    label_encoder = None
    symptom_list = []
    precautions_dict = {}
    print(f"ERROR: Could not load symptom model: {e}")


def general_test_view(request):
    """Display the symptom selection form."""
    # Format symptoms for display (replace underscores with spaces, capitalize)
    formatted_symptoms = []
    for symptom in symptom_list:
        display_name = symptom.replace('_', ' ').strip().title()
        formatted_symptoms.append({
            'value': symptom,
            'display': display_name
        })
    
    return render(request, 'welcome/general_test.html', {
        'title': 'General Health Test',
        'symptoms': formatted_symptoms,
        'total_symptoms': len(symptom_list)
    })


@csrf_exempt
def predict_disease(request):
    """Predict disease based on selected symptoms."""
    if request.method != 'POST':
        return redirect('general_test')
    
    # Get selected symptoms from form
    selected_symptoms = request.POST.getlist('symptoms')
    
    if not selected_symptoms:
        return render(request, 'welcome/general_test.html', {
            'title': 'General Health Test',
            'symptoms': [{'value': s, 'display': s.replace('_', ' ').strip().title()} for s in symptom_list],
            'total_symptoms': len(symptom_list),
            'error': 'Please select at least one symptom.'
        })
    
    if symptom_model is None:
        return render(request, 'welcome/disease_result.html', {
            'title': 'Prediction Error',
            'error': 'Model not loaded. Please try again later.'
        })
    
    # Create feature vector
    symptom_to_idx = {symptom: idx for idx, symptom in enumerate(symptom_list)}
    feature_vector = np.zeros(len(symptom_list), dtype=int)
    
    for symptom in selected_symptoms:
        symptom = symptom.strip()
        if symptom in symptom_to_idx:
            feature_vector[symptom_to_idx[symptom]] = 1
    
    # Get prediction probabilities
    probabilities = symptom_model.predict_proba([feature_vector])[0]
    
    # Get top 5 predictions
    top_indices = np.argsort(probabilities)[-5:][::-1]
    
    predictions = []
    for idx in top_indices:
        disease = label_encoder.inverse_transform([idx])[0]
        prob = probabilities[idx] * 100
        
        # Get precautions for this disease
        precs = precautions_dict.get(disease, [])
        if not precs:
            # Try matching with slightly different names
            for key in precautions_dict.keys():
                if key.lower().strip() == disease.lower().strip():
                    precs = precautions_dict[key]
                    break
        
        predictions.append({
            'disease': disease,
            'probability': round(prob, 2),
            'precautions': precs
        })
    
    # Format selected symptoms for display
    selected_display = [s.replace('_', ' ').strip().title() for s in selected_symptoms]
    
    # SAUVEGARDER EN BASE DE DONNEES SI CONNECTÉ
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            GeneralResult.objects.create(
                user_profile=user_profile,
                selected_symptoms=selected_symptoms,
                predicted_diseases=predictions[:5] # Save top 5
            )
        except Exception as e:
            print(f"Erreur sauvegarde general result: {e}")

    return render(request, 'welcome/disease_result.html', {
        'title': 'Disease Prediction Results',
        'predictions': predictions,
        'selected_symptoms': selected_display,
        'symptom_count': len(selected_symptoms)
    })

# ===== CARDIOVASCULAR DISEASE PREDICTION =====

# Load cardio prediction model
try:
    cardio_model = joblib.load(os.path.join(symptom_model_dir, 'cardio_model.pkl'))
    cardio_scaler = joblib.load(os.path.join(symptom_model_dir, 'cardio_scaler.pkl'))
    cardio_features = joblib.load(os.path.join(symptom_model_dir, 'cardio_features.pkl'))
    print("Cardio prediction model loaded successfully.")
except FileNotFoundError as e:
    cardio_model = None
    cardio_scaler = None
    cardio_features = []
    print(f"ERROR: Could not load cardio model: {e}")


def formulaire_cardio(request):
    """Display the cardiovascular disease risk assessment form."""
    return render(request, 'welcome/cardio_form.html', {
        'title': 'Cardiovascular Disease Risk Assessment'
    })


@csrf_exempt
def predict_cardio(request):
    """Predict cardiovascular disease risk based on user inputs."""
    if request.method != 'POST':
        return redirect('formulaire_cardio')
    
    if cardio_model is None:
        return render(request, 'welcome/cardio_result.html', {
            'title': 'Prediction Error',
            'error': 'Model not loaded. Please try again later.'
        })
    
    try:
        # Get form data
        age_years = float(request.POST.get('age', 0))
        gender = int(request.POST.get('gender', 1))
        height = float(request.POST.get('height', 170))
        weight = float(request.POST.get('weight', 70))
        ap_hi = float(request.POST.get('ap_hi', 120))
        ap_lo = float(request.POST.get('ap_lo', 80))
        cholesterol = int(request.POST.get('cholesterol', 1))
        gluc = int(request.POST.get('gluc', 1))
        smoke = int(request.POST.get('smoke', 0))
        alco = int(request.POST.get('alco', 0))
        active = int(request.POST.get('active', 1))
        
        # Calculate BMI
        bmi = weight / ((height / 100) ** 2)
        
        # Create feature array in correct order
        features = [age_years, gender, height, weight, ap_hi, ap_lo, 
                   cholesterol, gluc, smoke, alco, active, bmi]
        
        # Scale features
        features_scaled = cardio_scaler.transform([features])
        
        # Get prediction and probability
        prediction = cardio_model.predict(features_scaled)[0]
        probability = cardio_model.predict_proba(features_scaled)[0][1] * 100
        
        # Determine risk level
        if probability >= 70:
            risk_level = 'High Risk'
            risk_class = 'high'
        elif probability >= 40:
            risk_level = 'Moderate Risk'
            risk_class = 'medium'
        else:
            risk_level = 'Low Risk'
            risk_class = 'low'
        
        # Precautions based on risk factors
        precautions = []
        if ap_hi >= 140 or ap_lo >= 90:
            precautions.append("Monitor your blood pressure regularly and consult a doctor about hypertension management")
        if cholesterol > 1:
            precautions.append("Follow a low-cholesterol diet and consider medication if recommended by your doctor")
        if bmi >= 25:
            precautions.append("Work on maintaining a healthy weight through balanced diet and regular exercise")
        if smoke == 1:
            precautions.append("Stop smoking - it significantly increases cardiovascular disease risk")
        if alco == 1:
            precautions.append("Limit alcohol consumption to reduce cardiovascular strain")
        if active == 0:
            precautions.append("Increase physical activity - aim for at least 30 minutes of moderate exercise daily")
        if gluc > 1:
            precautions.append("Monitor blood glucose levels and maintain a balanced diet")
        if age_years >= 50:
            precautions.append("Schedule regular cardiovascular check-ups with your healthcare provider")
        
        if not precautions:
            precautions.append("Maintain your healthy lifestyle and continue regular check-ups")
        
        # User inputs for display
        user_inputs = {
            'age': int(age_years),
            'gender': 'Female' if gender == 1 else 'Male',
            'height': height,
            'weight': weight,
            'bmi': round(bmi, 1),
            'systolic_bp': ap_hi,
            'diastolic_bp': ap_lo,
            'cholesterol': ['Normal', 'Above Normal', 'Well Above Normal'][cholesterol - 1],
            'glucose': ['Normal', 'Above Normal', 'Well Above Normal'][gluc - 1],
            'smoking': 'Yes' if smoke else 'No',
            'alcohol': 'Yes' if alco else 'No',
            'active': 'Yes' if active else 'No'
        }
        

        
        # SAUVEGARDER EN BASE DE DONNEES SI CONNECTÉ
        if request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                CardioResult.objects.create(
                    user_profile=user_profile,
                    input_data=user_inputs,
                    result_data={
                        "probability": probability,
                        "risk_level": risk_level,
                        "risk_class": risk_class,
                        "precautions": precautions
                    }
                )
            except Exception as e:
                print(f"Erreur sauvegarde cardio: {e}")

        return render(request, 'welcome/cardio_result.html', {
            'title': 'Cardiovascular Risk Assessment Results',
            'probability': round(probability, 1),
            'risk_level': risk_level,
            'risk_class': risk_class,
            'precautions': precautions,
            'user_inputs': user_inputs
        })
        
    except Exception as e:
        return render(request, 'welcome/cardio_result.html', {
            'title': 'Prediction Error',
            'error': f'An error occurred: {str(e)}'
        })
