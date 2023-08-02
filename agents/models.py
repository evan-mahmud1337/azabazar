from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from products.models import Products
from django.db.models.signals import post_save
from django.dispatch import receiver

class Agent(models.Model):
    profile = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    is_agent = models.BooleanField(default=False)
    def __str__(self):
        return self.profile.username

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    shop = models.IntegerField(blank=True, default=0)
    income= models.IntegerField(blank=True, default=0)
    cash = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    wallet = models.CharField(max_length=20)
    agent = models.ForeignKey(
                                Agent, on_delete=models.CASCADE, blank=True, null=True,
                                )
    home_del = models.CharField(blank=True, max_length=20)
    product = models.CharField(max_length=200)
    qty = models.IntegerField()
    total = models.FloatField()
    unit_price = models.IntegerField(blank=True, default=0)
    address = models.CharField(max_length=300, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True,null=True, default="pending")

    def __str__(self):
        return self.user.username

