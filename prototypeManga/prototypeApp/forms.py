from django import forms
from django.core.exceptions import ValidationError


def validate_uniprotID(value):
    valid_lengths = [6, 10]
    if len(value) not in valid_lengths:
        raise ValidationError('The uniprot ID must be either 6 or 10 characters long.')    

class ProteinInputForm(forms.Form):
    uniprot_id = forms.CharField(label='Enter an UniProt ID: ',max_length=10, validators=[validate_uniprotID])
    

    