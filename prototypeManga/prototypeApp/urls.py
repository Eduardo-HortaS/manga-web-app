from django.urls import path 
from . import views

urlpatterns = [
    path('', views.proteinInstantiationView, name='prototype'),
    path('results/<str:acession_id_value>', views.resultsView, name='results'),
]
