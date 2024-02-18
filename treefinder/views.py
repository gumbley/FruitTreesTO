from django.shortcuts import render
from .models import Tree
from django.core.serializers import serialize
from django.http import JsonResponse
import json
from datetime import datetime

def home(request):
    trees = serialize('json', Tree.objects.all())
    return render(request, 'treefinder/home.html', {'trees': trees})

def get_trees_within_bounds(request):
    ne_lat = request.GET.get('neLat')
    ne_lng = request.GET.get('neLng')
    sw_lat = request.GET.get('swLat')
    sw_lng = request.GET.get('swLng')
    name = request.GET.get('name')
    in_season = request.GET.get('inSeason') == 'true'

    # Define fruit groupings
    fruit_groupings = {
        'Apple': ['Apple', 'Apple, common'],
        'Apricot': ['Apricot'],
        'Cherry': ['Cherry', 'Cherry, black', 'Cherry, sweet'],
        'Mulberry': ['Mulberry', 'Mulberry, red', 'Mulberry, white', 'Mulberry, white weeping'],
        'Peach': ['Peach'],
        'Pear': ['Pear'],
        'Plum': ['Plum', 'Plum, Canada'],
        'Serviceberry': [ 'Serviceberry', 'Serviceberry Robin hill', 'Serviceberry, smooth'],
    }

    trees = Tree.objects.filter(
        latitude__lte=ne_lat, latitude__gte=sw_lat,
        longitude__lte=ne_lng, longitude__gte=sw_lng
    )

    if name and name != 'all':
        specific_fruits = fruit_groupings.get(name, [name])
        trees = trees.filter(name__in=specific_fruits)
    
    if in_season:
        today = datetime.now().timetuple().tm_yday
        trees = trees.filter(fruiting_start_day__lte=today, fruiting_end_day__gte=today)

    trees_data = serialize('json', trees)
    trees_list = json.loads(trees_data)
    return JsonResponse(trees_list, safe=False)