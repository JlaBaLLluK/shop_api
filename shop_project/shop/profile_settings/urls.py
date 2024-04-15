from django.contrib.auth.decorators import login_required
from django.urls import path
from profile_settings.views import *

urlpatterns = [
    path('change-password/', ChangePasswordView.as_view()),
    path('change-username/', ChangeUsernameView.as_view()),
    path('delete-account/', DeleteProfileView.as_view()),
    path('change-first-last-name/', ChangeFirstLastNameView.as_view()),
    path('change-email/', ChangeEmailView.as_view())
]
