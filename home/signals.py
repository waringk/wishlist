# Citation for the following code:
# Date: 3/12/2022
# Modified from:
# Source URL: https://dev.to/earthcomfy/django-user-profile-3hik

# this file is used to modify or create a DB entry based on an event

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserSettings
from django.db import models
from django.contrib.auth.models import User



# creates a profile for a user
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(user=instance)

# modifies a profile for a user
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.user_settings.save()