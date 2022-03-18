# Citation for the following code:
# Date: 3/12/2022
# Modified from:
# Source URL: https://tutorial.djangogirls.org/en/django_urls/


# this file assigns views to URLs, and uses the Django URL resolver to direct the page navigation
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import HomePageView, WishListView, WishListSearchResultsView, ItemSearchPageView, UserSettingsView


urlpatterns = [

    # view for items that contain a tag
    path('wishlist/tags/<str:tag>/', views.wish_list_item_tag_results, name='wish_list_item_tag_results'),

    # view for adding a wish list item
    path('wishlist/add', views.wish_list_add_from_form, name='wish_list_add'),

    # view for wish list item details
    path('wishlist/<int:id>/', views.wish_list_item_details, name='wish_list_item_details'),

    # view to delete a wish list item
    path('delete/<int:id>/', views.delete, name='delete'),

    # view to confirm wish list item delete
    path('deleteconfirm/<int:id>/', views.deleteconfirm, name='deleteconfirm'),

    # view for item search
    path('item_search/', ItemSearchPageView.as_view(), name='item_search'),

    # view for wish list items
    path("wishlist/", views.wish_list_add_from_search, name="wishlist"),

    # view for searching the wish list
    path("wish_list_search_results/", views.wish_list_search, name="wish_list_search_results"),

    # view for searching for an item from external retailers
    path("item_search_results/", views.item_search_results, name="item_search_results"),

    # home page view
    path("", HomePageView.as_view(), name="home"),

    # user settings menu view
    path("user_settings/", views.user_settings, name="user_settings"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

