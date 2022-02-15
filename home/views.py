# view is where we put the logic of the application
# create a view
# will request information from the model and pass it to a template
# connects content (models saved in database) and display it in template
# if there is no post with given pk, display Page Not Found 404 page

from django.shortcuts import render, get_object_or_404

# import redirect to redirect a user to a newly created page
from django.shortcuts import redirect

import json

from .forms import WishListForm

from django.db.models import Q
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import TemplateView, ListView

from .models import WishListItem, WishListItemTag, WishListTagQuantity

# from .forms import DeleteWishListItem


from time import sleep


class HomePageView(TemplateView):
    template_name = 'base.html'


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


def wish_list_add(request):
    context = {}
    context['form'] = WishListForm
    if request.method == 'POST':
        WishListAdd = WishListForm(request.POST)
        if WishListAdd.is_valid():

            f = open("microservice.txt", "w")
            f.write('#' + WishListAdd.data.get('name'))
            f.close()
            response = ''
            while True:
                f = open("microservice.txt", "r")
                response = f.readline()
                f.close()
                if response and response[0] != '#':
                    break
                sleep(0.05)

            item = WishListAdd.save(commit=False)
            item.save()
            tag_qty = 0
            new_tags = []
            json_object = json.loads(response)
            for word_info in json_object:
                tag_qty += 1
                if tag_qty <= 10:
                    new_tag = WishListItemTag()
                    new_tag.name = word_info['word']
                    new_tag.save()
                    new_tags.append(new_tag)
                else:
                    break

            for tag in new_tags:
                item.tags.add(tag)

            return HttpResponseRedirect('/wishlist/')
    else:
        return render(request, "wishlistadd.html", context)


def wish_list_item_tag_results(request, tag):
    qty = WishListTagQuantity.objects.filter(tag__name=tag).all()
    #print(qty[0].item.id)
    data = []
    for item in qty:
        data.append(WishListItem.objects.get(id=item.item.id))

    return render(request, 'wishlistitemtagsresults.html',
                  {"object_list": data, "tag_name": tag})


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


def wish_list_update_tags(request, id):
    wish_list_item = WishListItem.objects.get(id=id)
    # return render(request, 'wishlistitemdetails.html', {'object_list': [wish_list_item]})
    # return render(request, 'wishlistitemdetails.html',
    # {"object_list": [{"id": id, "tags": WishListItem.objects.get(id=id).tags}]})

    return render(request, 'wishlistitemdetails.html',
                  {"object_list": [{"id": id, "tags": WishListItem.objects.get(id=id).tags}]})
