from django.shortcuts import render
from .models import Tree

def home(request):
    return render(request, 'treefinder/home.html')
