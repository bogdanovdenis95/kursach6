from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import SomeModel
from mailings.models import Mailing, Client
from blog.models import BlogPost
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)
@login_required
def home(request):
    total_mailings = Mailing.objects.count()
    active_mailings = 0
    unique_clients = Client.objects.values('email').distinct().count()
    random_posts = BlogPost.objects.order_by('?')[:3]
    
    user_is_manager = request.user.groups.filter(name='Manager').exists()
    
    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
        'random_posts': random_posts,
        'user_is_manager': user_is_manager,
    }
    return render(request, 'main/home.html', context)


@login_required
def users(request):
    return render(request, 'main/users.html')


@login_required
def mailings(request):
    return render(request, 'main/mailings.html')
