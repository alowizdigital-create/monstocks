from django import forms
from .models import Product, Category ,Article,Unit

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "unit",
            "sale_price",
            "quantity"
        ]

class CategoryForm(forms.ModelForm):
    class Meta:
        model =  Category
        fields = [
            "name",
        ]
        


class ArticleForm(forms.ModelForm):
    class Meta:
        model =  Article
        fields = [
            "name",'create_id'
        ]


class UnitForm(forms.ModelForm):
    class Meta:
        model =  Unit
        fields = [
            "name",'symbol'
        ]
