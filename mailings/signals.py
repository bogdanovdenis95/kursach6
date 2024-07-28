# mailings/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Mailing, Client, Message

@receiver(pre_save, sender=Mailing)
def set_owner_for_mailing(sender, instance, **kwargs):
    if instance.pk is None and hasattr(instance, 'request'):
        instance.owner = instance.request.user

@receiver(pre_save, sender=Client)
def set_owner_for_client(sender, instance, **kwargs):
    if instance.pk is None and hasattr(instance, 'request'):
        instance.owner = instance.request.user

@receiver(pre_save, sender=Message)
def set_owner_for_message(sender, instance, **kwargs):
    if instance.pk is None and hasattr(instance, 'request'):
        instance.owner = instance.request.user
