# view is where we put the logic of the application
# create a view
# will request information from the model and pass it to a template

from django.shortcuts import render

# post_list takes a request and returns the value it gets from render
# renders the template blog/post_list.html
def post_list(request):
    return render(request, 'blog/post_list.html', {})