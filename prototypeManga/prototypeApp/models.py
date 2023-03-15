from django.db import models
from .forms import UniprotForm

# Create your models here.
# 
class UniProt(models.Model):
    id = UniprotForm.id()
    