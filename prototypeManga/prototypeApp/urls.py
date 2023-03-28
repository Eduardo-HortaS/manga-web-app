from django.urls import path 
from . import views

urlpatterns = [
    path('', views.ProteinInstantiationView, name='prototype'),
    path('results/<int:acession_id_value>', views.resultsView, name='results'),
]
