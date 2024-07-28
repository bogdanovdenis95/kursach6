# users/urls.py

from django.urls import path
from .views import UserUpdateView, user_list, block_user, register, verify_email, login_view, success_view, error_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/users/login/'), name='logout'),
    path('verify-email/', verify_email, name='verify_email'),
    path('success/', success_view, name='success_url'),
    path('error/', error_view, name='error_url'),
    path('edit/<int:pk>/', UserUpdateView.as_view(), name='edit_user'),
    path('', user_list, name='user_list'), 
    path('block/<int:user_id>/', block_user, name='block_user'),
]

