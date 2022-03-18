# Citation for the following code:
# Date: 3/12/2022
# Modified from:
# Source URL: https://tutorial.djangogirls.org/en/django_forms/

# This file creates a form for adding and editing our models

from django import forms
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from .models import WishListItem, WishListItemTag, WishListTagQuantity, User, UserSettings


class WishListForm(forms.ModelForm):
    # tell Django to use the wish list item model to create the form

    selected = models.BooleanField(default=False)
    selected.required = False

    class Meta:
        model = WishListItem
        # specify the fields that should be on the form
        fields = ('name', 'price', 'item_url', 'item_photo', 'store')


# Citation for the following code:
# Date: 3/12/2022
# Modified from:
# Source URL: https://stackoverflow.com/questions/1075314/allow-changing-of-user-fields-like-email-with-django-profiles

class UserSettingsForm(forms.ModelForm):
    # tell Django to use the user settings model to create the form

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        # specify the fields that should be on the form
        model = UserSettings
        fields = ['name', 'email']

    def save(self, *args, **kwargs):
        settings = super(UserSettingsForm, self).save(*args, **kwargs)
        return settings


class UpdateProfileForm(forms.ModelForm):
    # tell Django to use the user settings model to create the form
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        # specify the fields that should be on the form
        model = UserSettings
        fields = ['bio']
