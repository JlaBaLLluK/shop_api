from django.urls import path
from registration.views import *

urlpatterns = [
    path('user-registration/', UserRegistrationView.as_view()),
]
