from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from .forms import CustomUserCreationForm, UserUpdateForm
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseForbidden

User = get_user_model()

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

@user_passes_test(is_manager)
@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

@user_passes_test(is_manager)
@login_required
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    return redirect('user_list')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
            user.email_verification_token = token
            user.email_verification_expiry = timezone.now() + timezone.timedelta(hours=1)
            user.save()
            send_mail(
                'Verify your email',
                f'Your verification token is {token}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            return redirect('verify_email')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def verify_email(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        try:
            user = CustomUser.objects.get(email_verification_token=token)
            if user.email_verification_expiry < timezone.now():
                return redirect('error_url')

            user.is_active = True
            user.email_verified = True
            user.save()
            auth_login(request, user)
            return redirect('success_url')
        except CustomUser.DoesNotExist:
            return redirect('error_url')
    return render(request, 'verify_email.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.groups.filter(name='Manager').exists():
                return redirect('user_list')
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def success_view(request):
    return render(request, 'success.html')

def error_view(request):
    return render(request, 'error.html')


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'edit_user.html'
    success_url = reverse_lazy('user_list')

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs['pk'])
