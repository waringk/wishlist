
# this file is used to add, edit and delete wish list items that we've modeled
# import/include the model, and make our model visible on the admin page

from django.contrib import admin
from .models import WishListItem, WishListItemTag, UserSettings

admin.site.register(UserSettings)


# handles many to many relationship between items and tags
class TaginWishListItemInline(admin.TabularInline):
    model = WishListItem.tags.through


# import model and put it in admin
@admin.register(WishListItem)
class WishListItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    inlines = [
        TaginWishListItemInline
    ]


# import model and put it in admin
@admin.register(WishListItemTag)
class WishListItemTagAdmin(admin.ModelAdmin):
    field = "name"
