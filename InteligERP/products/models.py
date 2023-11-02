from django.db import models
from stakeholders.models import Supplier
from storage.models import Section

# Create your models here.
class Object(models.Model):
	product_id = models.IntegerField(null=True,unique=True)
	name = models.CharField(max_length=200)
	height = models.DecimalField(max_digits=20,decimal_places=3)
	length = models.DecimalField(max_digits=20,decimal_places=3)
	width = models.DecimalField(max_digits=20,decimal_places=3)
	weight = models.DecimalField(max_digits=20,decimal_places=3)
	supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,verbose_name="the supplier of the product",default=1)
	section = models.ForeignKey(Section, on_delete=models.CASCADE,verbose_name="the section where the product is stored",default=1)
	#price ?