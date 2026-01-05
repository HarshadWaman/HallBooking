from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def avhalls(request):
    return render(request, 'avhalls.html')

def landing(request):
    return render(request, 'landing.html')