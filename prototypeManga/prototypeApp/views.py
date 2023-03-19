import json
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import uniprotID
from .models import uniprotData
from django.core.exceptions import ValidationError


# Create your views here.
def prototype(request):
    #form = uniprotID()
    if request.method == 'POST':
        form = uniprotID(request.POST)
        if form.is_valid():
            #protein_instance = uniprotData(id=form.cleaned_data('uniprot_id'))
            form.save()
        url = f'https://rest.uniprot.org/uniprotkb/search?query={uniprot_id}'
        response = requests.get(url)
        if response.status_code != 200:
            raise ValidationError('Error connecting to UniProt API.')
        data = response.json()
        protein_instance = uniprotData(
            id=form.cleaned_data('uniprot_id'),
            name=data['results'][0]['proteinDescription']['recommendedName']['fullName']['value'], 
            sequence=data['results'][0]['sequence']['value'], 
            features=data['results'][0]['features'],
            )
        print(protein_instance)
        return HttpResponseRedirect(reverse('results', protein_instance)) # COMO FAÇO PARA PODER MANDAR PROTEIN_INSTANCE PARA O RESULTSVIEW?
        #return render(request, 'results.html', {'id': protein_instance.id, 'name': protein_instance.name, 'sequence': protein_instance.sequence, 'features': protein_instance.features})
    else:
        form = uniprotID()
    return render(request, 'form.html', {'form': form})

    
def resultsView(request):
    return render(request, 'results.html', {'id': protein_instance.id, 'name': protein_instance.name, 'sequence': protein_instance.sequence, 'features': protein_instance.features})

    # show database instances
    
    

    # url = f'https://rest.uniprot.org/uniprotkb/search?query={uniprot_id}'
    # response = requests.get(url)
    # if response.status_code != 200:
    #     raise ValidationError('Error connecting to UniProt API.')
    # #data = json.loads(response.text)
    # data = response.json()       
    # #if 'primaryAccession' not in data or data['entryType'] == 'Inactive':
    # #    raise ValidationError('Invalid UniProt ID.')
    # return render(request, 'form.html', {'form': form})