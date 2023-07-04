from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    mail = models.CharField(max_length=200)
    password = models.CharField(max_length=30)
    date_created = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    dni = models.IntegerField()
    docket = models.IntegerField()
    birth_date = models.DateTimeField()