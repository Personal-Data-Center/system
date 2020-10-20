from django.db import models

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=30)
    docker_id= models.CharField(max_length=30)
    path = models.CharField(max_length=30)
    icon = models.CharField(max_length=30)
