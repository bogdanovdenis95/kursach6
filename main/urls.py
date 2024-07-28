# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('other/', views.other_view, name='other_view'),
]
