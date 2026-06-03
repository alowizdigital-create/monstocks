from django.urls import path
from .views import *


urlpatterns = [
    path("", order_list, name="order_list"),
    path('pos/', pos, name="pas"),
    path('invoice/<int:sale_id>/', invoice, name="invoice"),
    path('create-order/', create_order, name="create_order"),
    path('detail/<uuid:uuid>/', order_detail, name='order_detail'),
    path('send/<uuid:uuid>/', order_send, name='order_send'),
    path('delivry/<uuid:uuid>/', order_delivry, name='order_delivry'),
]
