from django.shortcuts import render
from django.http import HttpResponse

# function to return render of chatroom.html
def index(request):
    return render(request, 'chatroom.html')
