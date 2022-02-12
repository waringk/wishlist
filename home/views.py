# view is where we put the logic of the application
# create a view
# will request information from the model and pass it to a template
# connects content (models saved in database) and display it in template
# if there is no post with given pk, display Page Not Found 404 page

from django.shortcuts import render, get_object_or_404

# import redirect to redirect a user to a newly created page
from django.shortcuts import redirect



from django.db.models import Q
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import TemplateView, ListView

from .models import WishListItem
# from .forms import DeleteWishListItem

from .forms import WishListForm


class HomePageView(TemplateView):
    template_name = 'home.html'


class ItemSearchPageView(TemplateView):  # new
    template_name = "itemsearch.html"


class WishListView(ListView):
    model = WishListItem
    template_name = 'wishlist.html'


class WishListSearchResultsView(ListView):
    model = WishListItem
    template_name = 'wish_list_search_results.html'

    # receives the search query from the user for searching within wish list items
    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        object_list = WishListItem.objects.filter(Q(name__icontains=query))
        return object_list


def delete_queryset1(request, id):
    wish_list_item = get_object_or_404(WishListItem, id=id)

    if request.method == 'POST':
        wish_list_item.delete()
        return redirect('wishlist')

    return render(request, 'wishlistdelete.html', {'WishListItems': wish_list_item})


@csrf_exempt  # Add this too.
def delete(request, id):
    return render(request, 'wishlistdelete.html',
                  {"object_list": [{"id": id, "name": WishListItem.objects.get(id=id).name}]})


@csrf_exempt  # Add this too.
def deleteconfirm(request, id):
    if request.method == 'POST':  # <- Checking for method type
        print("r=", request.POST)
        WishListItem.objects.get(id=id).delete()
    return HttpResponseRedirect('/wishlist/')


# displays the wish list item details - name and price
def wish_list_items(request):
    wish_list = WishListItem.objects.all()
    print("Length of wish list:", len(wish_list))
    for item in wish_list:
        print(item)
    return render(request, 'wishlist.html', {'WishListItems': wish_list})


def wish_list_item_details(request, id):
    wish_list_item = WishListItem.objects.get(id=id)
    return render(request, 'wishlistitemdetails.html', {'object_list': [wish_list_item]})

def wish_list_item_details_tags(request, id):
    wish_list_item = WishListItem.objects.get(id=id)
    return render(request, 'wishlistitemdetails.html', {'object_list': [wish_list_item]})



