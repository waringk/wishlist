# import Django forms
from django import forms
from django.db import models
from django.views.decorators.csrf import csrf_exempt

from .models import WishListItem, WishListItemTag, WishListTagQuantity


class WishListForm(forms.ModelForm):
    # tell Django which model should be used to create the form

    selected = models.BooleanField(default=False)
    selected.required = False

    class Meta:
        model = WishListItem
        # specify the fields that should be on the form
        fields = ('name', 'price')


