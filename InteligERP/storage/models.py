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
	height = models.DecimalField(max_digits=20,decimal_places=3)
	length = models.DecimalField(max_digits=20,decimal_places=3)
	width = models.DecimalField(max_digits=20,decimal_places=3)
	max_weight = models.DecimalField(max_digits=20,decimal_places=3,null=True)
	description = models.CharField(max_length=300,null=True)
	available_storage = models.DecimalField(max_digits=20,decimal_places=3,default=0)
	
	"""def save(self, *args, **kwargs):
		self.available_storage = self.height * self.length * self.width
		super(Section, self).save(*args, **kwargs)"""