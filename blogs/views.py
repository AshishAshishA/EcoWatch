from django.shortcuts import render, get_object_or_404, HttpResponse
from django.db.models import F
from django.urls import reverse, reverse_lazy

from .models import Category, Post, Comment
from .forms import PostForm, CommentForm

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView


class ListBlogs(ListView):
    model = Post
    template_name='list_blog.html'
    context_object_name='blogs'
    paginate_by = 3



    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)

        context['cat']=''
        context['categories'] = Category.objects.all()
        context['latest_id'] = -1
        print(self.kwargs)
        if 'id' in self.kwargs.keys():
            print('here')
            latest_id = context['latest_id'] = self.kwargs['id']
            latest_blog = context['latest_blog'] = (Post.objects.filter(id=self.kwargs['id']).values())[0]
            print(f'latest_id is : {latest_id}')
            print(f'latest_blog is : {latest_blog}')

        return context

showListOfAllBlogs = ListBlogs.as_view()

class ListBlogByCategory(ListView):
    model = Post
    template_name='list_blog.html'
    context_object_name='blogs'
    paginate_by = 3

    def __init__(self):
        self.cat=None                    # cat -> category

    def get_queryset(self):
        self.cat = self.kwargs.get('category')
        if self.cat:
            return Post.objects.filter(categories__name__iexact=self.cat)
        else:
            return super().get_queryset()

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)

        context['cat']=self.cat
        context['categories'] = Category.objects.all()

        return context

showListByCategory=ListBlogByCategory.as_view()

class DetailPostViewWithCommentForm(CreateView):
    model=Comment
    form_class=CommentForm
    template_name='detail_blog.html'
    # success_url=''

    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        # print(self.kwargs)
        post = Post.objects.filter(id=self.kwargs.get('id'))
        comments = Comment.objects.filter(post=(post.values())[0].get('id')).values()
        # print(post)
        post.update(views=F('views')+1)
        context['blog'] = post[0]
        print(post[0])
        context['comments'] = comments
        
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        
        post_id = self.kwargs.get('id')
        post = get_object_or_404(Post, id=post_id)
        
        kwargs['post'] = post
        return kwargs
    
    def get_success_url(self):

        return reverse('detail', args=[self.kwargs['slug'], self.kwargs['id']])

detailPostWithComments = DetailPostViewWithCommentForm.as_view()

class CreateBlogs(CreateView):
    model=Post
    form_class=PostForm
    template_name='create_blog.html'
    
    def get_success_url(self,*args,**kwargs):
        created_post = self.object
        return reverse('home-updated', args=[created_post.id, created_post.slug])

createBlogs = CreateBlogs.as_view()

class UpdateBlogsView(UpdateView):
    model=Post
    form_class=PostForm
    template_name='create_blog.html'

    def get_success_url(self):

        return reverse('home-updated', args=[self.kwargs['id'],self.kwargs['slug']])

updateBlogsView = UpdateBlogsView.as_view()

class DeleteBlogsView(DeleteView):
    model=Post
    template_name='detail_blog.html'
    
    def get_success_url(self):

        return reverse_lazy('home')                                        

deleteBlogsView = DeleteBlogsView.as_view()


def generate_gpt_input_value(request):
    import os
    import ai21
    from ai21 import AI21Client

    AI21_API_KEY = os.environ.get('AI21_API_KEY')

    def get_safe_completion(prompt):
        print(f'inside completion {prompt}')

        client = AI21Client(
            # api_key='DyCMgHSZnyTAUwD1yKUfqwhUadC4xynU',
            api_key = AI21_API_KEY
        )
        completion = client.completion.create(
                model="j2-ultra",
                prompt=prompt,
                max_tokens=17,
                temperature=0.8,
            )
        
        first_completion = completion.completions[0]
        completion_text = first_completion.data.text

        print(f"completion text {completion_text}")

        return completion_text

    ai21.api_key = 'DyCMgHSZnyTAUwD1yKUfqwhUadC4xynU'
    if request.method == "POST":
        print('inside post')
        blog_post = request.POST.get('gpt-body')

        prompt = f"No pretext or explanations. Write a concise website blog post title for the following blog post:{blog_post}"
        completion = get_safe_completion(prompt)
        
        return render(request, 'ai_res.html', {'ai_title':completion})
    return render(request, 'ai_res.html', {'ai_title':'not generated'})