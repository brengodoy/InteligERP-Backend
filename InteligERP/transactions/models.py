from django.db import models
from stakeholders.models import Supplier,Client
from products.models import Object,Price
from django.utils import timezone
from django.db.models import Max

# Create your models here.
class Purchase(models.Model):
	date = models.DateTimeField(default=timezone.now,null=True)
	total_cost = models.DecimalField(max_digits=20,decimal_places=3,default=0)
	supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE,verbose_name="supplier related to the purchase",default=1)

class Sale(models.Model):
	date = models.DateTimeField(default=timezone.now)
	paid = models.BooleanField(default=False)
	client = models.ForeignKey(Client,on_delete=models.CASCADE,verbose_name="client related to the sale",default=1)

class Sale_object(models.Model):
	sale = models.ForeignKey(Sale,on_delete=models.CASCADE,verbose_name="sale",default=1)
	object = models.ForeignKey(Object,on_delete=models.CASCADE,verbose_name="object",default=1)
	amount = models.DecimalField(max_digits=20,decimal_places=2,default=1)

	class Meta:
		constraints = [
            models.UniqueConstraint(fields=['sale', 'object'], name='unique_sale_object')
        ]
class Purchase_object(models.Model):
	purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE,verbose_name="purchase",default=1)
	object = models.ForeignKey(Object,on_delete=models.CASCADE,verbose_name="object",default=1)
	amount = models.DecimalField(max_digits=20,decimal_places=2,default=1)
	price = models.DecimalField(max_digits=20, decimal_places=2, null=True) # blank = true permite que el campo price sea opcional
	#price = price.object = object and price.supplier = purchase.supplier
	#supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE,default=purchase.supplier)
	
	# def save(self, *args, **kwargs):
	# 	if not self.price:
	# 		price_object = Price.objects.filter(object=self.object, supplier=self.purchase.supplier).annotate(max_date=Max('date'))
	# 		#.last()
	# 		self.price = price_object.price * self.amount if price_object else 0
			
	# 		super(Purchase_object, self).save(*args, **kwargs)