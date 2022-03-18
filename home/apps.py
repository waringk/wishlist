# Citation for the following code:
# Date: 3/12/2022
# Modified from:
# Source URL: https://dev.to/earthcomfy/django-user-profile-3hik

# this file is used for application configuration

from django.apps import AppConfig


# user configuration
class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals


# wish list item configuration

class WishlistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wishlist'
