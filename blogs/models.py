from django.db import models

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=250)
    body = RichTextUploadingField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    slug=models.SlugField(max_length=250,blank=True,unique=False)
    views=models.IntegerField(null=True, default=0)

    categories  = models.ManyToManyField("Category" ,related_name="posts")

    class Meta:
        ordering = ['-views']
        get_latest_by = ['created_on']

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args,**kwargs)
        return self.slug

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    author = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    class Meta:
        get_latest_by = ["created",]
        ordering = ['created']
    
    def __str__(self):
        return f"{self.post} by {self.author}"