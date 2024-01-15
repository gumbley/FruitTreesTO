from django.shortcuts import render
from .models import Tree
from django.core.serializers import serialize
from django.http import JsonResponse
import json

def home(request):
    trees = serialize('json', Tree.objects.all())
    return render(request, 'treefinder/home.html', {'trees': trees})

def get_trees_within_bounds(request):
    ne_lat = request.GET.get('neLat')
    ne_lng = request.GET.get('neLng')
    sw_lat = request.GET.get('swLat')
    sw_lng = request.GET.get('swLng')

    trees = Tree.objects.filter(
        latitude__lte=ne_lat,
        latitude__gte=sw_lat,
        longitude__lte=ne_lng,
        longitude__gte=sw_lng
    )
    trees_data = serialize('json', trees)
    trees_list = json.loads(trees_data)  # Parse the JSON string back into a Python object
    return JsonResponse(trees_list, safe=False)  # Pass the Python object to JsonResponse