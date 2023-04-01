from django.shortcuts import render
import requests

def chat(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        print('Sending message:', message)
        response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={'message': message})
        print('Received response:', response.json())

    return render(request, 'index.html')
