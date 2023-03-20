from django.db import models
from .forms import uniprotID

# A model that stores the id and data associated with it for processing. 
class proteinBaseData(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.TextField()
    sequence = models.TextField()
    
class proteinFeatures(models.Model):
    id = models.ForeignKey(proteinBaseData, on_delete=models.CASCADE)
    feature_type = models.CharField(max_length=255)
    feature_description = models.CharField(max_length=255)
    feature_start = models.IntegerField()
    feature_end = models.IntegerField()
