# this file is used to add, edit and delete posts that we've modeled
# import/include the Post model
# make our model visible on the admin page

from django.contrib import admin

from .models import WishListItem, WishListItemTag


class TaginWishListItemInline(admin.TabularInline):
    model = WishListItem.tags.through


@admin.register(WishListItem)
class WishListItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    inlines = [
        TaginWishListItemInline
    ]


@admin.register(WishListItemTag)
class WishListItemTagAdmin(admin.ModelAdmin):
    field = "name"
