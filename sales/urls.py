from django.urls import path
from .views import *


urlpatterns = [
    path("", sale_list, name="sale_list"),
    path("create/", sale_create, name="sale_create"),
    path("cashbox/", cashbox_create, name="cashbox_create"),
    path("cashbox_list/", cashbox_list, name="cashbox_list"),
    path('pos/', pos, name="pos"),
    path('invoice/<int:sale_id>/', invoice, name="invoice"),
    path('create-sale/', create_sale, name="create_sale"),
]

