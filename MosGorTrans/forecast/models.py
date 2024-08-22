from django.db import models

# Create your models here.
class homes(models.Model):
    apart = models.IntegerField()
    flats = models.IntegerField()
    office = models.IntegerField()