from django.urls import path
from .views import *

urlpatterns = [
    path("", product_list, name="product_list"),
    path("create/", product_create, name="product_create"),
    path("categories/", category_list, name="category_list"),
    path("categories/create/", category_create, name="category_create"),
    path("categories/delete/<int:id>/", category_delete, name="category_delete"),
    path("categories/edit/<int:id>/", category_edit, name="category_edit"),
    path("units/create", unit_create, name="unit_create"),
    path("units/", unit_list, name="unit_list"),
    path("units/delete/<int:id>/", unit_delete, name="unit_delete"),
    path('<uuid:uuid>/', product_detail, name='product_detail'),
    path('<uuid:uuid>/edit/', product_edit, name='product_edit'),
]

