from django.db import models

# Create your models here.
class Warehouse(models.Model):
	id_warehouse = models.IntegerField(null=True)
	name = models.CharField(max_length=300)
	address = models.CharField(max_length=400)
	description = models.CharField(max_length=400,null=True)

class Section(models.Model):
	warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,verbose_name="the related warehouse",default=1)
	id_section = models.IntegerField(null=True)
	height = models.IntegerField()
	length = models.IntegerField()
	width = models.IntegerField()
	max_weight = models.IntegerField(null=True)
	description = models.CharField(max_length=300,null=True)