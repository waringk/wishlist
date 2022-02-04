# import Django forms
from django import forms

# import our Post model
from .models import Post

# name of form is PostForm
# PostForm is a ModelForm, will save the result of the form to the model
# use the form in a view and display it in a template
class PostForm(forms.ModelForm):

    # tell Django which model should be used to create the form
    # uses model Post
    class Meta:
        model = Post

        # specify the fields that should be on the form
        fields = ('title', 'text',)