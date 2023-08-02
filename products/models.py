from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    class Meta:
        ordering = ('title', )
    def  __str__(self):
        return self.title

class Products(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit_point = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.title

class Offers(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, default=0)
    selling_price = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
class OfferImage(models.Model):
    image = models.ImageField(upload_to='products/')
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name