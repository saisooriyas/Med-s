from django.urls import path
from . import views

urlpatterns = [

    path('about/',views.about,name='about'),
    path('chat/', views.chat, name='chat'),
    path('contact/', views.contact, name='contact'),
    path('contactus/', views.contactus, name='contactus'),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('services/', views.services, name='services'),
]
