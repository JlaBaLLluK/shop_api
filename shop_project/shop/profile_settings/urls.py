from django.contrib.auth.decorators import login_required
from django.urls import path
from profile_settings.views import *

urlpatterns = [
    path('change-password/', ChangePasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('change-username/', ChangeUsernameView.as_view()),
    path('delete-account/', DeleteProfileView.as_view()),
    path('change-other-information/', ChangeOtherInformationView.as_view()),
]
