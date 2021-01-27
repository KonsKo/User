from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from django.forms import ValidationError


User = get_user_model()

class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email',
                  'phone', 'address', 'password1', 'password2', 'photo']


class CustomAuthenticationForm(AuthenticationForm):

    class Meta:
        model = User

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError('There was a problem with your login.')


class ReSendConfEmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError('Email does not exist')
        else:
            user = User.objects.filter(email=email).first()
            if user.is_active == True:
                raise ValidationError('Your account is already active')
        return email







