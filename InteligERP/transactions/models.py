from django.db import models
from stakeholders.models import Supplier,Client
from products.models import Object
from django.utils import timezone

# Create your models here.
class Purchase(models.Model):
	date = models.DateTimeField(default=timezone.now,null=True)
	total_cost = models.DecimalField(max_digits=20,decimal_places=3,null=True)
	supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE,verbose_name="supplier related to the purchase",default=1)

class Sale(models.Model):
	date = models.DateTimeField(default=timezone.now,null=True)
	paid = models.BooleanField(default=False)
	client = models.ForeignKey(Client,on_delete=models.CASCADE,verbose_name="client related to the sale",default=1)

	class Meta:
		constraints = [
            models.UniqueConstraint(fields=['date', 'client'], name='unique_date_client')
        ]

class sale_object(models.Model):
	sale = models.ForeignKey(Sale,on_delete=models.CASCADE,verbose_name="sale",default=1)
	object = models.ForeignKey(Object,on_delete=models.CASCADE,verbose_name="object",default=1)
	amount = models.DecimalField(max_digits=20,decimal_places=2,default=1)

	class Meta:
		constraints = [
            models.UniqueConstraint(fields=['sale', 'object'], name='unique_sale_object')
        ]


