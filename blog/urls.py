
# importing Django's function path and all of our views from the blog application
from django.urls import path
from . import views

# add our first URL pattern
# assign a view called post_view to the root URL
# matches an empty string and the Django URL resolver will ignore the domain name that prefixes the URL path
# tells Django that views.post_list is the right place to go if someone enters 'http://127.0.0.1:8000/' address.
# name='post_list' is the name of the URL to identify the view
urlpatterns = [
    path('', views.post_list, name='post_list'),

    #create a URL to a post's detail
    # URL in blog/urls.py points to a view named post_detail that will show a blog post
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    # create a URL to add a blog post
    # URL in blog/urls.py points to a view named post_new that will add a new blog post
    path('post/new/', views.post_new, name='post_new'),

    # create a URL to edit a blog post
    # URL in blog/urls.py points to a view named post_edit that will edit a blog post
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
]