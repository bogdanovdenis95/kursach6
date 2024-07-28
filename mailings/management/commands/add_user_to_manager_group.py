from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Add a user to the "Manager" group'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username of the user to be added to the group')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            manager_group = Group.objects.get(name='Manager')
            user.groups.add(manager_group)
            self.stdout.write(self.style.SUCCESS(f'User "{username}" added to the "Manager" group'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" does not exist'))
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Group "Manager" does not exist'))
