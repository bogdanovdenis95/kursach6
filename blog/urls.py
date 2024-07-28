# blog/urls.py
from django.urls import path
from .views import blog_list, blog_detail, home

app_name = 'blog'

urlpatterns = [
    path('', home, name='home'),
    path('posts/', blog_list, name='blog_list'),
    path('posts/<int:pk>/', blog_detail, name='blog_detail'),
]
