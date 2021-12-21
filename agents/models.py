from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

class Agent(models.Model):
    profile = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    is_agent = models.BooleanField(default=False)
    def __str__(self):
        return self.profile.username

