from django.conf import settings
from django.db import models


class WishListItemTag(models.Model):
    verbose_name = "WishListItemTags"
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class WishListItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    verbose_name = "WishListItems"
    selected = models.BooleanField(default=False)
    selected.required = False
    tags = models.ManyToManyField(WishListItemTag, through='WishListTagQuantity')

    def __str__(self):
        return self.name


class WishListTagQuantity(models.Model):
    tag = models.ForeignKey(WishListItemTag, on_delete=models.CASCADE)
    item = models.ForeignKey(WishListItem, on_delete=models.CASCADE)
    extra_tags = models.BooleanField(default=False)
