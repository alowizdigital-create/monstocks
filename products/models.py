from django.db import models
from core.models import BaseModel, Company
import uuid


class Category(BaseModel):
    name = models.CharField(max_length=150)
    company_id = models.IntegerField()

    def __str__(self):
        return self.name


class Unit(BaseModel):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    company_id = models.IntegerField()

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    company_id = models.IntegerField()
    quantity = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Article(models.Model):
    name = models.CharField(max_length=200)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    create_id = models.IntegerField()

    def __str__(self):
        return self.name

class Movement(BaseModel):
    type = models.CharField(max_length=50)
    amount =  models.DecimalField(max_digits=10, decimal_places=2,default=0)
    quantity = models.IntegerField()
    company_id = models.IntegerField()
    product_id = models.IntegerField()

    def __str__(self):
        return self.type



    