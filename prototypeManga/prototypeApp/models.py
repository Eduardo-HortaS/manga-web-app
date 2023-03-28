from django.db import models

# A model that stores the id and data associated with it for processing. 
class Protein(models.Model):
    acession_id = models.CharField(max_length=10, unique=True)
    name = models.TextField()
    sequence = models.TextField()
    
class FeatureType(models.Model):
    value = models.CharField(max_length=255, null=True, blank=False) # Eduardo: parece que temos casos onde é nulo...
    
class Feature(models.Model):
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE)
    feature_type = models.ForeignKey(FeatureType, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    start = models.IntegerField(null=True, blank=False)
    end = models.IntegerField(null=True, blank=False)
