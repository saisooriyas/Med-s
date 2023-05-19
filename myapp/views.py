import requests
from bson import ObjectId
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from pymongo import MongoClient
from myapp.models import CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from myapp.models import Profile
from pymongo import MongoClient
import hashlib

def about_view(request):
    return render(request, 'about.html')

def home_view(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

def contact_us(request):
    return render(request, 'contactus.html')

def services(request):
    return render(request, 'services.html')


def chat(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        print('Sending message:', message)
        response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={'message': message})
        print('Received response:', response.json())
    if request.user.is_authenticated:
        return render(request, 'chat.html')
    return HttpResponse("Hi, you are not logged in.")


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        User1 = get_user_model()
        users = User1.objects.filter(email=email)

        if users.exists():
            user = users.first()  # Retrieve the first user if multiple users have the same email
            if user.check_password(password):
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('chat')

        context = {'error': 'Invalid email or password.'}
        return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')


def generate_user_id(email):
    # Generate unique ID based on email
    email_hash = hashlib.md5(email.encode()).hexdigest()
    return email_hash


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

        # Generate unique ID for the user
        user_id = generate_user_id(email)

        # Add user to database
        user_data = {
            'user_id': user_id,
            'email': email,
            'password': password,
            'phone_number': phone_number
        }
        users_collection.insert_one(user_data)

        # Create a new CustomUser instance
        user = CustomUser(user_id=user_id, email=email)
        user.set_password(password)
        user.save()

        # Create a new Profile instance
        profile = Profile(user=user, phone_number=phone_number)
        profile.save()

        return redirect('chat')  # Redirect to the login page
    else:
        return render(request, 'registration.html')


def logout_view(request):
    logout(request)
    return redirect('login')
