# this file is used to add, edit and delete posts that we've modeled
# import/include the Post model
# make our model visible on the admin page

from django.contrib import admin
from .models import Post

admin.site.register(Post)
