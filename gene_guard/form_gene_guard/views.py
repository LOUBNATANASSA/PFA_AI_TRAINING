from django.shortcuts import render, HttpResponse , redirect

# Create your views here.
def home(request):
    
    return render(request,'welcome/home.html',{'title':'GeneGuard'})
    
   


def formulaire(request):
    return render(request,'welcome/formulaire.html',{'title':'Formulaire'})


def resultat(request):
    return render(request,'welcome/resultat.html',{'title':'Resultat'})