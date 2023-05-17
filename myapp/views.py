from django.shortcuts import render
import requests

def chat(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        print('Sending message:', message)
        response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={'message': message})
        print('Received response:', response.json())

    return render(request, 'chat.html')

def login(request):
    return render(request,'login.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def contactus(request):
    return render(request,'contactus.html')

def index(request):
    return render(request,'index.html')

def register(request):
    return render(request,'register.html')

def services(request):
    return render(request, 'services.html')