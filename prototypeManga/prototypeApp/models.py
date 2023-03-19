from django.db import models
from .forms import uniprotID

# A model that stores the id and data associated with it for processing. 
class uniprotData(models.Model):
    id = models.CharField(max_length=10)
    name = models.TextField()
    sequence = models.TextField()
    features = models.TextField()