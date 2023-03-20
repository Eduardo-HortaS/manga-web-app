from django.urls import path 
from . import views

urlpatterns = [
    path('', views.prototype, name='prototype'),
    path('results/<int:pi_id>', views.resultsView, name='results'), # VOU PRECISAR MESMO DESSE OUTRO VIEW, OU TERIA UMA FORMA MAIS SIMPLES DE RENDERIZAR UMA PÁGINA DE RESULTADOS DENTRO DA MESMA VIEW?
]
