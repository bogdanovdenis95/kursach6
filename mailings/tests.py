from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Mailing, Message

CustomUser = get_user_model()

class ManagerAccessTest(TestCase):
    def setUp(self):
        self.manager_group = Group.objects.create(name='Менеджер')
        self.manager_user = CustomUser.objects.create_user(
            username='manager', 
            email='manager@example.com', 
            password='password'
        )
        self.manager_user.groups.add(self.manager_group)
        self.client.login(username='manager', password='password')

        self.regular_user = CustomUser.objects.create_user(
            username='regular', 
            email='regular@example.com', 
            password='password'
        )
        self.message = Message.objects.create(subject='Test message', body='This is a test message body', owner=self.regular_user)
        self.mailing = Mailing.objects.create(
            start_time='2023-01-01 00:00:00+00:00',  # Убедитесь, что используется aware datetime
            periodicity='DAILY',
            status='CREATED',
            message=self.message,
            owner=self.regular_user
        )

    def test_manager_can_view_mailings(self):
        response = self.client.get(reverse('mailings:mailing_list'))
        self.assertEqual(response.status_code, 200)

    def test_manager_cannot_edit_mailings(self):
        response = self.client.get(reverse('mailings:mailing_update', args=[self.mailing.id]))
        self.assertEqual(response.status_code, 403)

    def test_manager_can_block_user(self):
        response = self.client.post(reverse('mailings:block_user', args=[self.regular_user.id]))
        self.regular_user.refresh_from_db()
        self.assertFalse(self.regular_user.is_active)

    def test_manager_can_disable_mailing(self):
        response = self.client.post(reverse('mailings:disable_mailing', args=[self.mailing.id]))
        self.mailing.refresh_from_db()
        self.assertEqual(self.mailing.status, 'DISABLED')
