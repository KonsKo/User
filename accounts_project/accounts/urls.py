from django.urls import path
from django.contrib.auth.views import *
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from accounts.views import *

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('', TemplateView.as_view(template_name='base.html'), name='home'),

    path('password/',
         CustomPasswordChangeView.as_view(), name='password'),
    path('password/reset/',
         PasswordResetView.as_view(template_name='accounts/password_reset_form.html'),
         name='password_reset'),
    path('password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password/reset/done/',
         PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('password/reset/complete/',
         PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),

    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('cabinet/', login_required(CabinetView.as_view()), name='cabinet'),
    path('cabinet/update/photo', login_required(UpdatePhotoView.as_view()), name='update_photo'),
]
