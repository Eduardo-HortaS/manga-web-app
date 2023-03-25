import json
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .forms import uniprotID
from .models import Protein, FeatureType, Feature
from django.core.exceptions import ValidationError


# TODO: Você pode mover parte das operações pra outros arquivos, principalmente coisas que podem ser 
# reutilizadas mais pra frente, como por exemplo acessar APIs
# TODO: Nome dessa vista também não condiz com o papel dela
def prototype(request):
    if request.method == 'POST':
        form = uniprotID(request.POST)
        if form.is_valid():
            form.save() # TODO: Não entendi o que está sendo salvo aqui, já que sua classe não está associada a nenhum model
        url = f'https://rest.uniprot.org/uniprotkb/{form.uniprot_id}.json' #TODO: Erro de logica, tem que usar o cleaned_data igual vc fez na linha #26. Pega o accession e salva numa variavel pra não precisar chamar o cleaned_data mais de uma vez
        response = requests.get(url)
        if response.status_code != 200:
            # TODO: Se você der um raise aqui, seu servidor vai crashar, é isso realmente que você quer? Acho que é melhor mandar uma mensagem de erro na pagina dizendo que o UniProt não era valido
            raise ValidationError('Error connecting to UniProt API.')
        data = response.json()
        protein_instance = Protein(
            acession_id=form.cleaned_data('uniprot_id'),
            name=data['proteinDescription']['recommendedName']['fullName']['value'], 
            sequence=data['sequence']['value'], 
            )
        protein_instance.save()
        for feature in data['features']:
            # TODO: Tem certeza que esses campos estão sempre disponiveis? Caso contrario vai dar KeyError
            feature_type = feature['type']
            feature_description = feature['description']
            feature_start = feature['location']['start']['value']
            feature_end = feature['location']['end']['value']
        # TODO: Aqui tem um erro de logica. feature_type esta sendo lida dentro de um loop, quando você associa aqui por fora do loop, você está pegando só o último valor de feature_type
        pi_feature_type = FeatureType(
            value=feature_type
        )
        pi_feature_type.save()
        # TODO: O mesmo erro de logica citado acima, vali aqui também com feature_description, start e end.
        pi_feature = Feature(
            description=feature_description,
            start=feature_start,
            end=feature_end
        )
        pi_feature.save()
        
        return HttpResponseRedirect(reverse('results', kwargs = {'acession_id_value' : protein_instance.acession_id}))
    else:
        form = uniprotID()
    return render(request, 'form.html', {'form': form})

    
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
    return render(request, 'results.html', {'id': protein_instance.acession_id, 'name': protein_instance.name, 'sequence': protein_instance.sequence, 'feature_type': pi_features.feature_type, 'features': pi_features })

