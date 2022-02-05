# view is where we put the logic of the application
# create a view
# will request information from the model and pass it to a template
# connects content (models saved in database) and display it in template


from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home.html"


class ItemSearchPageView(TemplateView):  # new
    template_name = "itemsearch.html"

class WishListPageView(TemplateView):  # new
    template_name = "wishlist.html"

from django.shortcuts import render

# import timezone to publish home posts sorted by published date
from django.utils import timezone

# import the Post model
from .models import Post

# if there is no post with given pk, display Page Not Found 404 page
from django.shortcuts import render, get_object_or_404

# import redirect to redirect a user to a newly created page
from django.shortcuts import redirect

# import PostForm to construct the PostForm with data from a form
from .forms import PostForm


# post_list takes a request and returns the value it gets from render
# renders the template home/post_list.html+
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    # pass posts QuerySet to the template context
    # QuerySet: posts
    # returns the render function given the request from the user and
    # the template file 'home/post_list.html' and
    # things (posts) for the template to use
    return render(request, 'home/post_list.html', {'posts': posts})


# post's detail view, takes in the parameter pk for the post primary key
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'home/post_detail.html', {'post': post})


# form view to create a new Blog Post
# calls PostForm() and passes it to the template
# retrieve data in request.POST - contains the fields from the form


def post_new(request):
    # if we access the page for the first time, we want a blank form
    # otherwise, we want to send the form data to the view

    # if the method is POST, we construct the PostForm with the data form the form
    if request.method == "POST":
        form = PostForm(request.POST)

        # check that the form data is valid, and if so, we can save it
        # adds an author
        # commit=False means we dont want to save the Post model yet so we can add the author
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # redirects the user to the newly created home post in the post_detail page
            # redirects to the new home post based on primary key identifier
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'home/post_edit.html', {'form': form})


# similar method to post_new
# passes in pk parameter from URLs
def post_edit(request, pk):
    # get the Post model we want to edit
    post = get_object_or_404(Post, pk=pk)

    # when we create a form
    if request.method == "POST":
        # we pass this post as an instance when we save and when we open to edit
        form = PostForm(request.POST, instance=post)

        # validate the data before saving
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # then redirect the user to the post details
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'home/post_edit.html', {'form': form})
