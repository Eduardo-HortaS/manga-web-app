import json
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .forms import uniprotID
from .models import proteinBaseData, proteinFeatures
from django.core.exceptions import ValidationError


# Create your views here.
def prototype(request):
    if request.method == 'POST':
        form = uniprotID(request.POST)
        if form.is_valid():
            form.save()
        url = f'https://rest.uniprot.org/uniprotkb/search?query={form.uniprot_id}'
        response = requests.get(url)
        if response.status_code != 200:
            raise ValidationError('Error connecting to UniProt API.')
        data = response.json()
        protein_instance = proteinBaseData(
            id=form.cleaned_data('uniprot_id'),
            name=data['results'][0]['proteinDescription']['recommendedName']['fullName']['value'], 
            sequence=data['results'][0]['sequence']['value'], 
            )
        protein_instance.save()
        # Não tenho certeza se esse bloco pega todas as features de uma dada entrada. Ficaria
        # ruim por não ter algo que distingua as features dessa mesma entrada entre si?
        for feature in data['results'][0]['features']:
            feature_type = feature['type']
            feature_description = feature['description']
            feature_start = feature['location']['start']['value']
            feature_end = feature['location']['end']['value']
        protein_instance_feature = proteinFeatures(
            id = protein_instance.id,
            feature_type=feature_type,
            feature_description=feature_description,
            feature_start=feature_start,
            feature_end=feature_end
        )
        protein_instance_feature.save()
        return HttpResponseRedirect(reverse('results', kwargs = {'pi_id' : protein_instance.id}))
    else:
        form = uniprotID()
    return render(request, 'form.html', {'form': form})

    
def resultsView(request, pi_id):
    try:
        protein_instance = proteinBaseData.objects.get(pk=pi_id)
    except proteinBaseData.DoesNotExist:
        raise Http404('Protein instance does not exist.')
    # Como faço para acessar todas as features da entrada com foreign key = pi_id?
    # for proteinFeature in proteinFeatures.objects.get(id=pi_id): ?
    try:
        protein_instance_feature = proteinFeatures.objects.get(id=pi_id)  
    except proteinFeatures.DoesNotExist:
        raise Http404('Protein instance feature does not exist.')
    return render(request, 'results.html', {'id': protein_instance.id, 'name': protein_instance.name, 'sequence': protein_instance.sequence,}) # Colocar acesso a todas as features aqui, sequencialmente para uma dada id})


