from django.contrib.auth.decorators import login_required
from django.urls import path, include
from user.views import *


urlpatterns = [
    path('user-data/', UserView.as_view()),
]
