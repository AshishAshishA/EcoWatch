from django.contrib import admin
from .forms import PostForm
from .models import Post, Category, Comment
# Register your models here.

# admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Specify which fields to display in the form
    fields = ['title', 'body', 'categories','slug']
    
    # Hide the 'slug' field
    # exclude = ['slug']

    # readonly_fields = ['slug']

    prepopulated_fields = {'slug':('title',)}