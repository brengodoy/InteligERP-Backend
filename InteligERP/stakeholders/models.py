from django.db import models

# Create your models here.
class Client(models.Model):
    # Campos del modelo para Client
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    CUIL = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Supplier(models.Model):
    # Campos del modelo para Supplier
    company_name = models.CharField(max_length=255)
    CUIT = models.IntegerField()

    def __str__(self):
        return self.company_name
