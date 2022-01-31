from django.conf import settings
from django.db import models
from django.utils import timezone


# define our model object
# our model is Post
# models.Model tells Django that Post is a Django Model, so it will be saved in the database
class Post(models.Model):
    # define properties  of our Posts

    # models.ForeignKey - this is a link to another model
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # models.CharField - to define text with a limited number of characters
    title = models.CharField(max_length=200)

    # models.TextField - for long text without a limit
    text = models.TextField()

    # models.DateTimeField - for a date and time
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    # method to record a published date and save/publish the blog post
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # returns a string with a Post title
    def __str__(self):
        return self.title

