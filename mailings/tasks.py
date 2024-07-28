from datetime import datetime
import pytz
from django.core.mail import send_mail
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Mailing, MailingAttempt
import smtplib
from django.utils import timezone
from django.conf import settings



import logging

logger = logging.getLogger(__name__)

def send_mailing():
    zone = timezone.get_current_timezone()
    current_datetime = timezone.now()
    
    mailings = Mailing.objects.filter(start_time__lte=current_datetime, status='RUNNING')
    
    for mailing in mailings:
        last_attempt = MailingAttempt.objects.filter(mailing=mailing).order_by('-attempt_time').first()
        if last_attempt:
            time_since_last_attempt = current_datetime - last_attempt.attempt_time
            period_mapping = {
                'DAILY': timezone.timedelta(days=1),
                'WEEKLY': timezone.timedelta(weeks=1),
                'MONTHLY': timezone.timedelta(weeks=4)  # Простой подход для месячного периода
            }
            if time_since_last_attempt < period_mapping.get(mailing.periodicity, timezone.timedelta(days=1)):
                continue
        
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in mailing.clients.all()],
                fail_silently=False
            )
            MailingAttempt.objects.create(
                mailing=mailing,
                status='COMPLETED',
                server_response='Email sent successfully.'
            )
        except smtplib.SMTPException as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                status='FAILED',
                server_response=str(e)
            )

def should_send(periodicity, last_attempt_datetime, current_datetime):
    if periodicity == 'DAILY':
        return (current_datetime - last_attempt_datetime).days >= 1
    elif periodicity == 'WEEKLY':
        return (current_datetime - last_attempt_datetime).days >= 7
    elif periodicity == 'MONTHLY':
        return (current_datetime - last_attempt_datetime).days >= 30
    return False


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', minutes=1)  # Запуск каждые 1 минуту
    scheduler.start()
    print("Scheduler started") 

