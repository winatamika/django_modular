from django.db import models

# Create your models here.
class ModuleRegistry(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_installed = models.BooleanField(default=False)
    version = models.PositiveIntegerField(default=1)  # optional for upgrades
    
    
    