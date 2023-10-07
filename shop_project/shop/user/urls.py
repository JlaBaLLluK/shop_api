from django.contrib.auth.decorators import login_required
from django.urls import path, include
from user.views import *


urlpatterns = [
    path('<str:username>/', login_required(UserView.as_view(), login_url='#')),
    path('<str:username>/', include('profile_settings.urls')),
]
