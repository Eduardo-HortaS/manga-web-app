import json
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .forms import ProteinInputForm
from .models import Protein, FeatureType, Feature
from .general_utils import UniProtAPIResponseView

def ProteinInstantiationView(request):
    if request.method == 'POST':
        form = ProteinInputForm(request.POST)
        if form.is_valid():
            acession = form.cleaned_data['uniprot_id']
        if Protein.objects.filter(acession_id=acession).exists():     # Eduardo: coloquei no lugar certo? Parece dar erro 
           return HttpResponseRedirect(reverse('results', kwargs = {'acession_id_value' : acession}))  
        data = UniProtAPIResponseView(acession)
        protein_instance = Protein(
            acession_id=acession,
            name=data['proteinDescription']['recommendedName']['fullName']['value'], 
            sequence=data['sequence']['value'], 
            )
        protein_instance.save()
        for feature in data.get('features', {}):
            feature_type = feature.get('type')
            feature_description = feature.get('description')
            feature_location = feature.get('location', {})
            feature_start = feature_location.get('start', {}).get('value')
            feature_end = feature_location.get('end', {}).get('value')
            pi_feature_type = FeatureType(value=feature_type)
            pi_feature_type.save()
            pi_feature = Feature(description=feature_description, start=feature_start, end=feature_end)
            pi_feature.save()
        return HttpResponseRedirect(reverse('results', kwargs = {'acession_id_value' : protein_instance.acession_id}))
    else:
        form = ProteinInputForm()
    return render(request, 'form.html', {'form': form})

    
    # TODO: Isso está no local errado. Não faz parte da validação do form --- OK COLOCAR MAIS ACIMA DEPOIS
    # if Protein.objects.filter(id=value).exists():
    #     return HttpResponseRedirect(reverse('results', kwargs = {'pi_id' : value}))  
    
def resultsView(request, acession_id_value):
    try:
        protein_instance = Protein.objects.get(acession_id=acession_id_value)
    except Protein.DoesNotExist:
        raise Http404('Protein instance does not exist.')
    #protein_id = protein_instance.id
    # try:
    #     pi_feature_type = protein_instance.feature_type_set.all()
    # except FeatureType.DoesNotExist:
    #     raise Http404('Protein feature type does not exist.')
    try:
        pi_features = protein_instance.feature_set.all()
    except Feature.DoesNotExist:
        raise Http404('Protein instance feature does not exist.')
    return render(request, 'results.html', {'id': protein_instance.acession_id, 'name': protein_instance.name, 'sequence': protein_instance.sequence, 'feature_type and features': pi_features})

