from django.contrib.auth.decorators import login_required
from django.urls import path
from profile_settings.views import *

urlpatterns = [
    path('change-password/', login_required(ChangePasswordView.as_view(), login_url='login')),
    path('change-username/', login_required(ChangeUsernameView.as_view(), login_url='login')),
    path('delete-profile/', login_required(DeleteProfiledView.as_view(), login_url='login')),
]
