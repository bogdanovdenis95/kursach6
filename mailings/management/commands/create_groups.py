import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mailings.models import Mailing

class Command(BaseCommand):
    help = 'Create default groups and permissions'

    def handle(self, *args, **kwargs):
        # Create Manager group
        manager_group, created = Group.objects.get_or_create(name='Менеджер')
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Group "Менеджер" created'))
        else:
            self.stdout.write(self.style.WARNING(f'Group "Менеджер" already exists'))

        # Set permissions for Manager group
        content_type = ContentType.objects.get_for_model(Mailing)
        permissions = Permission.objects.filter(content_type=content_type, codename__in=[
            'view_mailing', 'view_client', 'view_message'
        ])
        
        for permission in permissions:
            manager_group.permissions.add(permission)
            self.stdout.write(self.style.SUCCESS(f'Permission "{permission.name}" added to group "Менеджер"'))
        
        self.stdout.write(self.style.SUCCESS('Default groups and permissions created'))
