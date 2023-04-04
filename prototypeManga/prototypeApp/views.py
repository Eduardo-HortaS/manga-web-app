import json
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.db import models
from .forms import ProteinInputForm
from .models import Protein, FeatureType, Feature
from .general_utils import uniProtAPIResponseView

def proteinInstantiationView(request):
    if request.method == 'POST':
        form = ProteinInputForm(request.POST)
        if form.is_valid():
            acession = form.cleaned_data['uniprot_id']            
            if Protein.objects.filter(acession_id=acession).exists():
                return redirect('prototypeApp:results', acession_id_value=acession)  
            data = uniProtAPIResponseView(acession)
            protein_instance = Protein(
                acession_id=acession,
                name=data['proteinDescription']['recommendedName']['fullName']['value'], 
                sequence=data['sequence']['value'], 
                )
            protein_instance.save() 
            for feature in data.get('features', {}):
                check = feature.get('type')
                if FeatureType.objects.filter(value=check).exists():
                    pi_feature_type = FeatureType.objects.get(value=check)
                else:
                    pi_feature_type = FeatureType(value=check)
                    pi_feature_type.save()
                feature_description = feature.get('description')
                feature_location = feature.get('location', {})
                feature_start = feature_location.get('start', {}).get('value')
                feature_end = feature_location.get('end', {}).get('value')
                pi_feature = Feature(protein=protein_instance, feature_type=pi_feature_type, description=feature_description, start=feature_start, end=feature_end)
                pi_feature.save()
            return redirect('prototypeApp:results', acession_id_value=acession)  
    else:
        form = ProteinInputForm()
    return render(request, 'form.html', {'form': form})
    
def resultsView(request, acession_id_value):
    try:
        protein_instance = Protein.objects.get(acession_id=acession_id_value)
    except Protein.DoesNotExist:
        raise Http404('Protein instance does not exist.')
    try:
        pi_features = Feature.objects.filter(protein__acession_id=acession_id_value)
    except Feature.DoesNotExist:
        raise Http404('No features associated to given UniProt ID.')
    return render(request, 'results.html', {'id': protein_instance.acession_id, 'name': protein_instance.name, 'sequence': protein_instance.sequence, 'pi_features': pi_features})

