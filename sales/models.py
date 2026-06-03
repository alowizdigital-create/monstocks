from django.db import models
from core.models import BaseModel, Company
from products.models import Product

# Create your models here.

class Sale(BaseModel):
    quantity =  models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    company_id = models.IntegerField()
    invoice_number = models.CharField(max_length=50, unique=True)  # numéro unique de facture

    def __str__(self):
        return self.product


class Cashbox(BaseModel):
    name = models.CharField(max_length=200)
    responsable_id = models.IntegerField()
    montant_initial = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    statut = models.CharField(max_length=20)
    company_id = models.IntegerField()

    def __str__(self):
         return self.name
    
    

class Item(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    

    