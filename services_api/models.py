from django.db import models

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=100, blank=False)
    docker_id= models.CharField(max_length=100, blank=False)
    image = models.CharField(max_length=100, blank=False)
    super = models.BooleanField(blank="false")
    is_required = models.BooleanField(blank="false")
    path = models.CharField(max_length=100, blank=False)
    icon = models.CharField(max_length=100, blank=False)
