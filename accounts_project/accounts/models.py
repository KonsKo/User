from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string

from phonenumber_field.modelfields import PhoneNumberField

from accounts.tasks import send_email_celery
from accounts.tokens import account_activation_token


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True, blank=False)
    date_create = models.DateTimeField(auto_now_add=True)
    address = models.CharField(blank=True, max_length=128)
    phone = PhoneNumberField(unique=True)
    photo = models.ImageField(upload_to='images/', blank=True)


    def __str__(self):
        return self.username

    def send_email(self):
        subject = 'Activate Your MySite Account'
        message = render_to_string('accounts/account_activation_email.html', {
            'user': self,
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(self.pk)),
            'token': account_activation_token.make_token(self),
        })
        to_email = self.email
        send_email_celery.delay(subject, message, to_email)



