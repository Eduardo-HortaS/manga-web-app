import json
import requests
from django.http import HttpResponse

def UniProtAPIResponseView(identifier):
    url = f'https://rest.uniprot.org/uniprotkb/{identifier}.json'
    response = requests.get(url)
    if response.status_code != 200:
        raise HttpResponse('Error connecting to UniProt API.')
    data = response.json()
    return data