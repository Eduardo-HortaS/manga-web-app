from django.contrib import admin
from .models import Protein, FeatureType, Feature

# Register your models here.
admin.site.register(Protein)
admin.site.register(FeatureType)
admin.site.register(Feature)
