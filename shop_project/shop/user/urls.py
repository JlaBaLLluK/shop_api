from django.contrib.auth.decorators import login_required
from django.urls import path
from user.views import *


urlpatterns = [
    path('<str:username>/', login_required(UserView.as_view(), login_url='#')),
]
