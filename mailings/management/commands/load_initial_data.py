from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Loads initial data from fixture files'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Scheduler started'))

        fixture_dir = os.path.join('mailings', 'fixtures')
        for fixture_file in os.listdir(fixture_dir):
            if fixture_file.endswith('.json'):
                fixture_path = os.path.join(fixture_dir, fixture_file)
                self.stdout.write(f'Loading fixture {fixture_path}')
                call_command('loaddata', fixture_path)

        self.stdout.write(self.style.SUCCESS('All fixtures loaded'))
