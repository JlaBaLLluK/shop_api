from django.urls import path
from emails.views import *

urlpatterns = [
    path('<int:pk>/send-verification-code/', SendVerificationCodeView.as_view())
]
