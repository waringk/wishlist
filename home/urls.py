
# importing Django's function path and all of our views from the home application
from django.urls import path
from . import views

from .views import HomePageView, WishListView, WishListSearchResultsView, ItemSearchPageView

# add our first URL pattern
# assign a view called post_view to the root URL
# matches an empty string and the Django URL resolver will ignore the domain name that prefixes the URL path
# tells Django that views.post_list is the right place to go if someone enters 'http://127.0.0.1:8000/' address.
# name='post_list' is the name of the URL to identify the view
urlpatterns = [


    path('wishlist/<int:id>/tags', views.wish_list_item_details_tags, name='wish_list_item_details_tags'),

    path('wishlist/<int:id>/', views.wish_list_item_details, name='wish_list_item_details'),

    path('delete/<int:id>/', views.delete, name='delete'),

    path('deleteconfirm/<int:id>/', views.deleteconfirm, name='deleteconfirm'),

    path('item_search/', ItemSearchPageView.as_view(), name='item_search'),

    path("wishlist/", WishListView.as_view(), name="wishlist"),

    path("wish_list_search_results/", WishListSearchResultsView.as_view(), name="wish_list_search_results"),

    path("", HomePageView.as_view(), name="home"),

]