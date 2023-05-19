from django.urls import path
from . import views

urlpatterns = [
    path('about/',views.about_view, name='about'),
    path('',views.home_view,name='home'),
    path('contact/',views.contact,name='contact'),
    path('contact_us/',views.contact_us,name='contact_us'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('chat/', views.chat, name='chat'),
    path('services/', views.services, name='services'),
    path('logout/', views.logout_view, name='logout'),
]
