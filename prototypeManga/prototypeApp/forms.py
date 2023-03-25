from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Protein


def validate_uniprotID(value):
    valid_lengths = [6, 10]
    if len(value) not in valid_lengths:
        raise ValidationError('The uniprot ID must be either 6 or 10 characters long.')
    if Protein.objects.filter(id=value).exists():
        return HttpResponseRedirect(reverse('results', kwargs = {'pi_id' : value}))

    

class uniprotID(forms.Form):
    uniprot_id = forms.CharField(label='Enter an UniProt ID: ',max_length=10, validators=[validate_uniprotID])
    

    