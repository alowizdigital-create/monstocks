from django.urls import path
from .views import *

urlpatterns = [
    path("", company_list, name="product_list"),
    path("create/", company_create, name="product_create"),
    path("categories/", category_list, name="category_list"),
    path("categories/create/", category_create, name="category_create"),

]