from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Assigns permissions to the manager group'

    def handle(self, *args, **kwargs):
        manager_group, created = Group.objects.get_or_create(name='Manager')

        permissions = [
            'view_mailing',
            'view_user',
            'can_disable_mailings',
        ]

        for perm in permissions:
            permission = Permission.objects.get(codename=perm)
            manager_group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Successfully assigned permissions to the manager group'))
