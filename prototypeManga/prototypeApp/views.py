import json
import requests
from django.shortcuts import render
from django.http import HttpResponseRedirect
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
        return render(request, 'form.html', {'form': form})
    else:
        form = uniprotID()
    
    
# def proteins(request):
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