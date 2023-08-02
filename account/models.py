from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.fields import CharField
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from agents.models import Wallet, Order
from products.models import Products
import random

class MyAccountManager(BaseUserManager):
    def create_user(self, address, nid_number, phone_number, username,refer,email, password=None):
        if not phone_number:
                raise ValueError('Users must have a phone number')
        user = self.model(
            address=address,
            nid_number=nid_number,
			phone_number=phone_number,
			username=username,
            refer=refer,
            email=email,
            password=password,
		)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, phone_number, username, address, nid_number,email,refer, password=None):
        user = self.create_user(
			phone_number=phone_number,
			password=password,
			username=username,
            address=address,
            nid_number=nid_number,
            email=email,
            refer=refer,
		)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email                 = models.EmailField(unique=True)
    address                 = models.CharField(max_length=300)
    date_joined             = models.DateField(auto_now_add=True, verbose_name="Joined time")
    last_login              = models.DateField(auto_now=True,verbose_name="Last loged in")
    phone_number            = models.CharField(max_length=14, unique=True)
    refer                   = models.CharField(max_length=14)
    nid_number              = models.CharField(max_length=30)
    username                = models.CharField(max_length=30)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    USERNAME_FIELD          = 'phone_number'
    REQUIRED_FIELDS         = ['username', 'address', 'nid_number', 'email', 'refer']


    objects = MyAccountManager()
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
    	return self.username

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, blank=False)
    phone_number = models.CharField(max_length=14)
    email = models.EmailField(blank=True, default='mmm@gmail.com')
    address = models.CharField(max_length=300)
    refer = models.CharField(max_length=14)
    def __str__(self):
    	return self.username

class Otp(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, null=True, blank=True)

    def save(self, *args, **kwargs):
        l = [x for x in range(10)]
        tp = []
        for i in range(6):
            num = random.choice(l)
            tp.append(num)
        otp_string = "".join(str(item) for item in tp)
        self.otp = otp_string    
        super().save(*args, **kwargs)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, raw=False, **kwargs):
    if created and not raw:
        Token.objects.create(user=instance)
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance= None, created=False, raw=False, **kwargs):
    if created and not raw:
        Profile.objects.create(user=instance, username=instance.username, phone_number=instance.phone_number,address=instance.address, refer=instance.refer, email=instance.email)
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_wallet(sender, instance= None, created=False, raw=False, **kwargs):
    if created and not raw:
        Wallet.objects.create(user=instance, shop=0,income=0,cash=0)
# @receiver(post_save, sender=Order)
# def create_units(sender, instance, created=False, **kwargs):
#     if created:
#         unit_point = Products.objects.filter(title=instance.product).first().unit_point
#         owa = Account.objects.filter(username=instance.user).first()
#         ow = Wallet.objects.get(user=owa)
#         owr = Account.objects.get(username=instance.user).refer
#         gone= Account.objects.filter(phone_number=owr).first()
#         gone_owr = Wallet.objects.get(user=gone)
#         gone_owr.income += unit_point
#         ow.income += unit_point
#         ow.save()
#         gone_owr.save()