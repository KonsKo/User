from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.encoding import force_text
from django.contrib.auth import login
from django.contrib.auth.views import *
from django.utils.http import urlsafe_base64_decode

from accounts.tokens import account_activation_token
from accounts.forms import *

User = get_user_model()

class CustomLoginView(SuccessMessageMixin, LoginView):
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('home')
    success_message = "You was logged in successfully"


class SignupView(SuccessMessageMixin, CreateView):

    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_message = "Your profile was created successfully"
    model = User

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.send_email()
            messages.success(request,
                             ('Please Confirm your email to complete registration.'))
            return redirect('login')
        else:
            render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('home')
        else:
            messages.warning(request,
                             ('The confirmation link was invalid, '
                              'possibly because it has already been used.'))
            return redirect('home')


class CabinetView(UpdateView):

    template_name = 'accounts/cabinet.html'
    model = User
    fields = ['phone',]

    def get_object(self):
        return self.request.user


class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):

    template_name = 'accounts/password_change_form.html'
    success_url = reverse_lazy('cabinet')
    success_message = "Password was changed successfully"


class UpdatePhotoView(SuccessMessageMixin, UpdateView):

    template_name = 'accounts/update_photo.html'
    model = User
    fields = ['photo',]
    success_url = reverse_lazy('cabinet')
    success_message = "Photo was changed successfully"

    def get_object(self):
        return self.request.user

class ReSendConfEmailView(FormView):
    form_class = ReSendConfEmailForm
    template_name = 'accounts/new_activate.html'
    success_url = reverse_lazy('login')
    success_message = "Check your email"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            user.send_email()
            messages.success(request, ('Check your email.'))
            return redirect('login')
        return render(request, self.template_name, {'form': form})



