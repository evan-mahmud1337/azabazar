from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.fields import CharField
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class MyAccountManager(BaseUserManager):
    def create_user(self, address, nid_number, phone_number, username, password, password2):
        if not phone_number:
                raise ValueError('Users must have a phone number')
        user = self.model(
            address=address,
			phone_number=phone_number,
			username=username,
            nid_number=nid_number,
            password=password,
            password2=password2,
		)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, phone_number, username, password, address, nid_number):
        user = self.create_user(
			phone_number=phone_number,
			password=password,
			username=username,
            address=address,
            nid_number=nid_number,
		)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email                 = models.EmailField(max_length=50, blank=True, null=True, default='email@gmail.com')
    address                 = models.CharField(max_length=300)
    date_joined             = models.DateField(auto_now_add=True, verbose_name="Joined time")
    last_login              = models.DateField(auto_now=True,verbose_name="Last loged in")
    phone_number            = models.CharField(max_length=14, unique=True)
    nid_number              = models.CharField(max_length=30)
    username                = models.CharField(max_length=30)
    password2               = models.CharField(max_length=20, default=False)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    USERNAME_FIELD          = 'phone_number'
    REQUIRED_FIELDS         = ['username', 'address', 'nid_number']


    objects = MyAccountManager()

    def __str__(self):
    	return self.username
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, blank=False)
    phone_number = models.CharField(max_length=14, unique=True)
    address = models.CharField(max_length=300)
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance= None, created=False, **kwargs):
    if created:
        Profile.objects.create(user=instance)
