# mailings/apps.py
from django.apps import AppConfig

class MailingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailings'

    def ready(self):
        import mailings.signals
        from .tasks import start_scheduler
        start_scheduler()
