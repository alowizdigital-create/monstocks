from django.db import models
from core.models import BaseModel
from products.models import Product



class Order(BaseModel):

    customer = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=150
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    note = models.TextField(
        blank=True,
        null=True
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=50,
        default='pending'
    )

    company_id = models.IntegerField()

    def __str__(self):
        return f"{self.customer} - {self.id}"


class OrderItem(BaseModel):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    custom_text = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.product.name