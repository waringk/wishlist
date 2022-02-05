
# importing Django's function path and all of our views from the home application
from django.urls import path
from . import views

from .views import HomePageView, ItemSearchPageView, WishListPageView

# add our first URL pattern
# assign a view called post_view to the root URL
# matches an empty string and the Django URL resolver will ignore the domain name that prefixes the URL path
# tells Django that views.post_list is the right place to go if someone enters 'http://127.0.0.1:8000/' address.
# name='post_list' is the name of the URL to identify the view
urlpatterns = [

    path("wishlist/", WishListPageView.as_view(), name="wishlist"),
    path("itemsearch/", ItemSearchPageView.as_view(), name="itemsearch"),
    path("", HomePageView.as_view(), name="home"),

    path('', views.post_list, name='post_list'),

    #create a URL to a post's detail
    # URL in home/urls.py points to a view named post_detail that will show a home post
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    # create a URL to add a home post
    # URL in home/urls.py points to a view named post_new that will add a new home post
    path('post/new/', views.post_new, name='post_new'),

    # create a URL to edit a home post
    # URL in home/urls.py points to a view named post_edit that will edit a home post
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
]