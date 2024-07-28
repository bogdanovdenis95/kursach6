# main/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import SomeModel
from mailings.models import Mailing, Client 
from blog.models import BlogPost 
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Кешируем на 15 минут
def home(request):
    total_mailings = Mailing.objects.count()
    active_mailings = 0
    unique_clients = Client.objects.values('email').distinct().count()
    random_posts = BlogPost.objects.order_by('?')[:3]
    
    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
        'random_posts': random_posts,
    }
    return render(request, 'main/home.html', context)
