import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from pymongo import MongoClient

from myapp.models import Profile


def chat(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        print('Sending message:', message)
        response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={'message': message})
        print('Received response:', response.json())
    if request.user.is_authenticated:
        return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat')
        else:
            context = {'error': 'Invalid email or password.'}
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        # Connect to MongoDB database
        client = MongoClient('mongodb://localhost:27017/')
        db = client['chatbot']
        users_collection = db['users']

        # Check if user already exists in database
        if users_collection.find_one({'email': email}) is not None:
            context = {'error': 'Email already exists.'}
            return render(request, 'registration.html', context)

        # Add user to database
        user_data = {
            'email': email,
            'password': password,
            'phone_number': phone_number
        }
        users_collection.insert_one(user_data)

        # Create Django User object
        user = User.objects.create_user(username=email, email=email, password=password,phone_number=phone_number)

        # Create Profile object and log user in
        profile = Profile.objects.create(user=user, phone_number=phone_number)
        login(request, user)
        return redirect('chat')
    else:
        return render(request, 'registration.html')


def logout_view(request):
    logout(request)
    return redirect('login')
