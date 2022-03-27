# this file contains the logic of the application to display the DB models in a template
# it creates views, requests information from the models and passes info to a template


import functools
import json
import threading
from multiprocessing import Process
from time import sleep

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from tutorial.tutorial.spiders.amazon import AmazonSpider
from tutorial.tutorial.spiders.walmart import WalmartSpider
from . import spider_spawner
from .forms import WishListForm, UserSettingsForm, NewUserForm
from .models import WishListItem, WishListItemTag, WishListTagQuantity, UserSettings, UserModel, User


class HomePageView(TemplateView):
    """Creates the home page view."""
    template_name = 'base.html'


class ItemSearchPageView(LoginRequiredMixin, TemplateView):
    """Creates the item search view for a user."""
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = "itemsearch.html"



@login_required(login_url='/accounts/login/')
def view_wish_list(request):
    """Creates the wish list view for a user with their own wish list."""
    context = {
        'object_list': WishListItem.objects.filter(user=request.user)
    }
    return render(request, 'wishlist.html', context)


class UserSettingsView(LoginRequiredMixin, ListView):
    """Creates the user settings menu for a user."""
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = UserSettings
    template_name = 'user_settings.html'


@login_required(login_url='/accounts/login/')
def user_settings(request):
    """Allows a user to update their user setting with a form. Uses UserSettingsForm for the logged in user. Captures
    POST data from the form, validates the input, and saves it to the user model."""

    if request.method == 'POST':
        form = UserSettingsForm(request.POST)
        if form.is_valid():
            found_id = None
            settings = None

            # user must already exist to update their info
            try:
                settings = UserSettings.objects.get(username__username=request.user)
            except UserSettings.DoesNotExist:
                settings = None
            if settings:
                found_id = settings.id

            # if user exists and entry is valid, update the user model info in DB
            form.instance.username = request.user
            if found_id:
                form.instance.id = found_id
            form.save()
            return render(request, 'user_settings.html', {'form': form})

        # render the page if the user tries to input invalid data
        else:
            return render(request, 'user_settings.html', {'form': form})

    else:
        settings = None
        form = None
        # user must already exist to update their info
        try:
            settings = UserSettings.objects.get(username__username=request.user)
        except UserSettings.DoesNotExist:
            settings = UserSettings()

        if settings is not None:
            if settings.email is None or len(settings.email) == 0:
                settings.email = request.user.email
                print("hello world")

        # update the user info if valid
        if settings:
            form = UserSettingsForm(instance=settings)
        else:
            form = UserSettingsForm
        # render the page if the user tries to input invalid data
        return render(request, "user_settings.html", {'form': form})


def register(request):
    """Allows a user to register an account on the website."""
    if request.method == "POST":

        form = NewUserForm(request.POST)
        if form.is_valid():

            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("wishlist/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()

    return render(request=request, template_name="registration/register.html", context={"register_form": form})


class WishListSearchResultsView(LoginRequiredMixin, ListView):
    """Creates search view for a user to search their wish list items."""
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = WishListItem
    template_name = 'wish_list_search_results.html'


def wish_list_search(request):
    """Receives the search query from the user for searching items in their wish list, and filters the DB for a
    certain item."""
    query = request.GET.get('q')

    qty = WishListItem.objects.filter(Q(name__icontains=query))
    print("qty =", qty)
    data = []
    for item in qty:
        # data.append(WishListItem.objects.get(id=item.id))
        data.append(item)
        print("item is", item)
    return render(request, "wish_list_search_results.html", {'object_list': data})


class ItemSearchResultsView(LoginRequiredMixin, ListView):
    """Creates search view for a user to search for items from big box retailers on external websites."""
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = WishListItem
    template_name = 'item_search_results.html'



crawler = None
class CrawlerScript(Process):
    """Creates asynchronous spiders from different retailers in different processes. Allows different processes to
    handle scraping from different retailers at the same time."""

    def __init__(self, spider):
        """Initialize a crawler process for a spider."""
        Process.__init__(self)
        settings = get_project_settings()
        self.crawler = CrawlerRunner(settings)
        # self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        self.spider = spider

    def run(self):
        """Run the created spider process."""
        self.crawler.crawl(type(self.spider))
        reactor.run()


def crawl_async():
    """Allows asynchronous spiders to process results at the same time."""
    spider = AmazonSpider()
    crawler = CrawlerScript(spider)
    crawler.start()
    crawler.join()


class SpiderThread(threading.Thread):
    """Creates a thread process for a spider. Allows each spider to run in its own thread. Takes input query text from
    the user for searching for an item."""

    def __init__(self, spider, query_text):
        """Initialize a spider thread."""
        super().__init__()
        self.done = False
        self.spider = spider
        self.query_text = query_text
        self.result = None

    def run(self):
        """Run the spider thread looking for the query text."""
        spider_spawner.run_spider(self.spider, self.query_text, self)
        self.done = True


def item_search_results(request):
    """Takes the input search from the user as a request and activates the web scraping spiders from Amazon and Walmart
    retail websites. Web scraping results are reduced to one result per process per retailer."""
    global crawler
    spiders = [AmazonSpider, WalmartSpider]
    results = []
    spider_spawner.test = []
    spider_threads = []

    # create a process for each spider with the inputted text
    for spider in spiders:
        new_thread = SpiderThread(spider, request.POST.get('q'))
        spider_threads.append(new_thread)
        new_thread.start()

    # prevents each spider from scraping many items/results from the same page
    # when the one result is found, stops the spiders from processing further
    while True:
        done_count = 0
        for i in range(len(spider_threads)):
            if spider_threads[i].done:
                done_count += 1
        if done_count == len(spider_threads):
            for i in range(len(spider_threads)):
                results.append(spider_threads[i].result)
            break
        sleep(0.05)

    def make_comparator(less_than):
        """Uses a comparator function to compare values in tuples. In the results, if the first is greater than the
        second it returns true, or false otherwise."""

        def compare(x, y):
            if less_than(x, y):
                return -1
            elif less_than(y, x):
                return 1
            else:
                return 0

        return compare


    def store_is_less_than(x, y):
        """Handles the race condition of returning results from different items in different retail stores. Sorts the
        results by store name."""
        return x['Store'] < y['Store']

    # sorts the results from different retail stores so they always appear in the same order
    sortedDict = sorted(results, key=functools.cmp_to_key(make_comparator(store_is_less_than)), reverse=False)
    return render(request, 'itemsearch.html', {"object_list": sortedDict, "q": request.POST.get('q')})


@login_required(login_url='/accounts/login/')
def add_search_result_to_list(request):
    """Adds an item search result to a user wishlist and renders the wish list page."""
    return render(request, "wishlistadd.html", [])


@login_required(login_url='/accounts/login/')
@csrf_exempt
def delete(request, id):
    """Filters for a wish list item by ID for the user to delete."""
    return render(request, 'wishlistdelete.html',
                  {"object_list": [{"id": id, "name": WishListItem.objects.get(id=id).name}]})


@login_required(login_url='/accounts/login/')
@csrf_exempt
def deleteconfirm(request, id):
    """Filters for a wish list item by ID for the user to delete to confirm the action. Then redirects the user back to
    the wishlist."""
    if request.method == 'POST':
        print("r=", request.POST)
        WishListItem.objects.get(id=id).delete()
    return HttpResponseRedirect('/wishlist/')


@login_required(login_url='/accounts/login/')
def wish_list_add_from_form(request):
    """Allows a user to add a wish list item with tags using a form. Automatically creates tags for the item based on
     data from a microservice. Captures POST data for the item entry and validates the data, and opens and reads/writes
     to a file to create tags based on item name. Redirects the user back to the updated wish list. """

    context = {}
    context['form'] = WishListForm

    if request.method == 'POST':
        WishListAdd = WishListForm(request.POST, request.FILES)

        # makes a request to the microservice to create tags data
        if WishListAdd.is_valid():

            f = open("microservice.txt", "w")
            f.write('#' + WishListAdd.data.get('name'))
            f.close()
            response = ''

            # read the response of data for tags from the microservice
            while True:
                f = open("microservice.txt", "r")
                response = f.readline()
                f.close()
                if response and response[0] != '#':
                    break
                sleep(0.05)

            item = WishListAdd.save(commit=False)

            item.photo_prefix = '/images/'
            item.user = request.user
            item.save()
            tag_qty = 0
            new_tags = []

            # parse the data for tag names and create the tags of words
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

            # add the tags to the item in the model, and redirect back to the wish list
            for tag in new_tags:
                item.tags.add(tag)
            item.item_photo = WishListAdd.cleaned_data['item_photo']

            return HttpResponseRedirect('/wishlist/')

        # if the entry is invalid, redirect back to the wish list
        else:
            return HttpResponseRedirect('/wishlist/')
    else:
        return render(request, "wishlistadd.html", context)


@login_required(login_url='/accounts/login/')
def wish_list_item_tag_results(request, tag):
    """Renders the results for filtering for a certain tag among the wish list items."""
    qty = WishListTagQuantity.objects.filter(tag__name=tag).all()
    data = []
    for item in qty:
        data.append(WishListItem.objects.get(id=item.item.id))
    return render(request, 'wishlistitemtagsresults.html', {"object_list": data, "tag_name": tag})


@login_required(login_url='/accounts/login/')
def wish_list_add_from_search(request):
    """Allows a user to add a wish list item from the item search view. Automatically creates tags for the item based on
     data from a microservice. Opens and reads/writes to a file to create tags based on item name. Logic will handle the
     item creation without tags if the microservice is not working. Redirects the user back to the updated wish list."""

    if request.method == 'POST':
        print("wish list add from search")
        WishListAdd = WishListItem()

        # makes a request to the microservice to create tags data
        f = open("microservice.txt", "w")
        f.write('#' + request.POST.get('name'))
        f.close()
        response = ''
        counter = 0
        skipTags = False

        # read the response of data for tags from the microservice
        while True:
            f = open("microservice.txt", "r")
            response = f.readline()
            f.close()
            if response and response[0] != '#':
                break
            # create items with empty tags if the microservice is down
            if counter >= 100:
                skipTags = True
                print("No response from microservice, is it down?")
                break
            counter += 1
            sleep(0.05)

        # get item data for putting into DB
        WishListAdd.name = request.POST.get('name')
        WishListAdd.price = request.POST.get('price').replace('$', '')
        if WishListAdd.price is None:
            WishListAdd.price = 0.0
        WishListAdd.item_url = request.POST.get('item_url')
        WishListAdd.item_photo = request.POST.get('item_photo')
        WishListAdd.store = request.POST.get('store')
        WishListAdd.user = request.user
        WishListAdd.save()
        tag_qty = 0
        new_tags = []

        # if the microservice is available, create tags of words and save the item model
        if not skipTags:
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
                WishListAdd.tags.add(tag)
        WishListAdd.save()

    wish_list = WishListItem.objects.all()
    for item in wish_list:
        print(item)
    return render(request, 'wishlist.html', {'object_list': wish_list})


@login_required(login_url='/accounts/login/')
def wish_list_item_details(request, id):
    """Renders an individual wish list item details page."""
    wish_list_item = WishListItem.objects.get(id=id)
    return render(request, 'wishlistitemdetails.html', {'object_list': [wish_list_item]})


@login_required(login_url='/accounts/login/')
def wish_list_item_details_tags(request, id):
    """Renders an individual wish list tags in the wish list item details page."""
    wish_list_item = WishListItem.objects.get(id=id)
    return render(request, 'wishlistitemdetails.html', {'object_list': [wish_list_item]})


@login_required(login_url='/accounts/login/')
def wish_list_update_tags(request, id):
    """Renders the wish list items with a particular tag."""
    return render(request, 'wishlistitemdetails.html',
                  {"object_list": [{"id": id, "tags": WishListItem.objects.get(id=id).tags}]})
