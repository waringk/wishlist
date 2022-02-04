# view is where we put the logic of the application
# create a view
# will request information from the model and pass it to a template
# connects content (models saved in database) and display it in template

from django.shortcuts import render

# import timezone to publish blog posts sorted by published date
from django.utils import timezone

# import the Post model
from .models import Post

# if there is no post with given pk, display Page Not Found 404 page
from django.shortcuts import render, get_object_or_404

from django.shortcuts import redirect
from .forms import PostForm

# post_list takes a request and returns the value it gets from render
# renders the template blog/post_list.html+
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    # pass posts QuerySet to the template context
    # QuerySet: posts
    # returns the render function given the request from the user and
    # the template file 'blog/post_list.html' and
    # things (posts) for the template to use
    return render(request, 'blog/post_list.html', {'posts': posts})


# post's detail view, takes in the parameter pk for the post primary key
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# view to create a new Post form and passes it to the template
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})