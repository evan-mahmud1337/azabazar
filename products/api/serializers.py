from django.db import models
from django.db.models import fields
from rest_framework import serializers
from products.models import Category, Products, Offers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('title', 'date', 'image', 'description', 'category', 'price', 'id')
class CategorySerializer(serializers.ModelSerializer):
    # product = ProductSerializer(many=True)
    class Meta:
        model = Category
        fields = (
            'title', 
            'date',
            'id',
            # 'product'
            )
class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = (
            'title', 
            'category', 
            'image', 
            'description', 
            'market_price', 
            'selling_price', 
            'date',
            'id',
            )