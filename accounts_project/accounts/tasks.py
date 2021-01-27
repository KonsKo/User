from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_email_celery(subject, message, to):
    email = EmailMessage(subject, message, to=[to, ])
    email.send()

#testing a scheduling
@shared_task
def send_email_all_users():
    EmailMessage('test', 'test', to=['konstantinkovalev88@gmail.com', ]).send()




