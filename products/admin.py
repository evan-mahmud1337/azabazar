from django.contrib import admin
from .models import Category, Products, Offers, OfferImage

admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Offers)
admin.site.register(OfferImage)
