from django.db import models

# A model that stores the id and data associated with it for processing. 
class Protein(models.Model):
    acession_id = models.CharField(max_length=10, unique=True)
    name = models.TextField()
    sequence = models.TextField(null=False, blank=False)
    
    def __str__(self) -> str:
        return f'{self.acession_id} \n {self.name} \n {self.sequence}' 
    
class FeatureType(models.Model):
    value = models.CharField(max_length=255, null=False, blank=False, unique=True)
    
    def __str__(self) -> str:
        return self.value
    
class Feature(models.Model):
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE)
    feature_type = models.ForeignKey(FeatureType, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    start = models.IntegerField(null=False, blank=False)
    end = models.IntegerField(null=False, blank=False)
    
    def __str__(self) -> str:
        #return f'{self.description} \n {self.start} \n {self.end}'
        return f'{self.protein} \n {self.feature_type} \n {self.description} \n {self.start} \n {self.end}'
