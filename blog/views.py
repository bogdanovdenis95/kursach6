# blog/views.py
from django.shortcuts import render, get_object_or_404
from .models import BlogPost
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)
def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog_list.html', {'posts': posts})

@cache_page(60 * 5)
def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.views += 1
    post.save()
    return render(request, 'blog_detail.html', {'post': post})

def home(request):
    return render(request, 'home.html')
