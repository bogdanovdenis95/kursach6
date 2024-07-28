from django.urls import path
from . import views

app_name = 'mailings'

urlpatterns = [
    path('', views.MailingListView.as_view(), name='mailing_list'),
    path('create/', views.MailingCreateView.as_view(), name='mailing_create'),
    path('<int:pk>/', views.MailingDetailView.as_view(), name='mailing_detail'),
    path('<int:pk>/edit/', views.MailingUpdateView.as_view(), name='mailing_update'),
    path('<int:pk>/delete/', views.MailingDeleteView.as_view(), name='mailing_delete'),
    path('<int:pk>/disable/', views.MailingDisableView.as_view(), name='disable_mailing'),
    path('messages/', views.MessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('messages/create/', views.MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/update/', views.MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', views.MessageDeleteView.as_view(), name='message_delete'),
    path('users/<int:pk>/block/', views.block_user, name='block_user'),
    path('manager/mailings/', views.ManagerMailingListView.as_view(), name='manager_mailing_list'),
    path('manager/mailings/<int:mailing_id>/disable/', views.disable_mailing, name='manager_disable_mailing'),
    path('reports/', views.MailingReportView.as_view(), name='mailing_report'),  # Путь к отчетам
]
