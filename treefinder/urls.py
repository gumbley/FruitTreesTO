from django.urls import path
from . import views
from .views import get_trees_within_bounds

urlpatterns = [
    path('', views.home, name='home'),
    path('api/trees', get_trees_within_bounds, name='get_trees_within_bounds'),
]
