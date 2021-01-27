from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email',
                  'phone', 'address', 'password1', 'password2', 'photo']


class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        print(user)
        if not user.is_active:
            raise forms.ValidationError('There was a problem with your login.')






