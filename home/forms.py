# This file creates a form for adding and editing our models

from django import forms
from django.contrib.auth.forms import UserCreationForm
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


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
