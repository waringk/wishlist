# this file stores our models of wish list items, wish list item tags, user settings

from django.conf import settings
from django.contrib.auth.backends import UserModel
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import User

# model for the user's settings
from mysite.settings import UPLOAD_ROOT


class UserSettings(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField('email', blank=True)
    username = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


# model for the wish list item tags
class WishListItemTag(models.Model):
    verbose_name = "WishListItemTags"
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


upload_storage = FileSystemStorage(location=UPLOAD_ROOT, base_url='/images')


# model for the wish list items
class WishListItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    verbose_name = "WishListItems"
    selected = models.BooleanField(default=False)
    selected.required = False
    tags = models.ManyToManyField(WishListItemTag, through='WishListTagQuantity')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True)
    item_url = models.CharField(max_length=200, null=True, blank=True)
    item_description = models.CharField(max_length=255, null=True, blank=True)
    item_photo = models.ImageField(upload_to='', null=True, blank=True, storage=upload_storage)
    photo_prefix = models.CharField(max_length=10, default='', blank=True)
    store = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


# model for handling the many to many wish list items/tags
class WishListTagQuantity(models.Model):
    tag = models.ForeignKey(WishListItemTag, on_delete=models.CASCADE)
    item = models.ForeignKey(WishListItem, on_delete=models.CASCADE)
    extra_tags = models.BooleanField(default=False)
