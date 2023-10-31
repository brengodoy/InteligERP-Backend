from django.db import models

# Create your models here.
class Warehouse(models.Model):
	id_warehouse = models.IntegerField(max_length=100)
	name = models.CharField(max_length=300)
	address = models.CharField(max_length=400)
	description = models.CharField(max_length=400)