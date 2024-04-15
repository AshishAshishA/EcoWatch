from django import forms
from ckeditor_uploader.fields import RichTextUploadingFormField
from .models import Post, Category, Comment
# from ckeditor_uploader.widgets import CKEditorUploadingWidget

class PostForm(forms.ModelForm):
    body = RichTextUploadingFormField()

    class Meta:
        model = Post
        fields = ['title', 'body', 'categories']
        widgets = {
            'categories': forms.SelectMultiple,  # Use forms.SelectMultiple widget for dropdown box
            "title": forms.TextInput( attrs={"class": "form-control", "autofocus": True, "id": "form-title"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the queryset for the categories field to use the Category model
        self.fields['categories'].queryset = Category.objects.all()

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['author','body','post']

        widgets = {
            'post': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        # Get the `post` parameter from kwargs
        post_instance = kwargs.pop('post', None)
        
        # Call the superclass constructor
        super().__init__(*args, **kwargs)
        
        # If a `post` instance is provided, set it as the initial value of the `post` field
        if post_instance is not None:
            self.fields['post'].initial = post_instance