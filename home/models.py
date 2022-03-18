# Citation for the following code:
# Date: 3/12/2022
# Modified from:
# Source URL: https://tutorial.djangogirls.org/en/django_models/

# Citation for the following code:
# Date: 3/12/2022
# Modified from:
# Source URL: https://www.sankalpjonna.com/learn-django/the-right-way-to-use-a-manytomanyfield-in-django

# Citation for the following code:
# Date: 3/12/2022
# Modified from:
# Source URL: https://stackoverflow.com/questions/43894232/displaying-both-sides-of-a-manytomany-relationship-in-django-admin


# this file stores our models of wish list items, wish list item tags, user settings

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


# model for the user's settings
class UserSettings(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField('email', unique=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    username = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


# model for the wish list item tags
class WishListItemTag(models.Model):
    verbose_name = "WishListItemTags"
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


# model for the wish list items
class WishListItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    verbose_name = "WishListItems"
    selected = models.BooleanField(default=False)
    selected.required = False
    tags = models.ManyToManyField(WishListItemTag, through='WishListTagQuantity')
    username = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    item_url = models.CharField(max_length=200, null=True, blank=True)
    item_description = models.CharField(max_length=255, null=True, blank=True)
    item_photo = models.ImageField(upload_to='wishlist/', null=True, blank=True)
    store = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


# model for handling the many to many wish list items/tags
class WishListTagQuantity(models.Model):
    tag = models.ForeignKey(WishListItemTag, on_delete=models.CASCADE)
    item = models.ForeignKey(WishListItem, on_delete=models.CASCADE)
    extra_tags = models.BooleanField(default=False)
