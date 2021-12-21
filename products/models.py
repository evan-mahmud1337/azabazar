from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Offers(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")
    description = models.TextField()
    market_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title