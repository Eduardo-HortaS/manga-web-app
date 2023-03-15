from django import forms

class UniprotForm(forms.Form):
    id = forms.CharField(max_length=10)
    

    