from django.db import models
from django.db.models import fields
from rest_framework import serializers
from products.models import Category, Products, Offers, OfferImage

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('title', 'date', 'image', 'description', 'category', 'price', 'selling_price', 'unit_point')
class CategorySerializer(serializers.ModelSerializer):
    # product = ProductSerializer(many=True)
    class Meta:
        model = Category
        fields = (
            'title', 
            'date', 
            'id',
            'image'
            # 'product'
            )
class OfferSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)
    class Meta:
        model = Offers
        fields = (
            'product',
            'selling_price', 
            'date'
            )
class OfferImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferImage
        fields = (
            'image',
            'name',
            )