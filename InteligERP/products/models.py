from django.db import models

# Create your models here.
class Object(models.Model):
	product_id = models.IntegerField(null=True,unique=True)
	name = models.CharField(max_length=200)
	height = models.DecimalField(max_digits=20,decimal_places=3)
	length = models.DecimalField(max_digits=20,decimal_places=3)
	width = models.DecimalField(max_digits=20,decimal_places=3)
	weight = models.DecimalField(max_digits=20,decimal_places=3)