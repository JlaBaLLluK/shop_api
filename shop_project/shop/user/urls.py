from django.contrib.auth.decorators import login_required
from django.urls import path
from user.views import *


urlpatterns = [
    path('<str:username>/', login_required(UserView.as_view(), login_url='#')),
    path('<str:username>/change-password/', login_required(ChangePasswordView.as_view(), login_url='#')),
    path('<str:username>/change-username/', login_required(ChangeUsernameView.as_view(), login_url='#')),
    path('<str:username>/delete-profile/', login_required(DeleteProfileView.as_view(), login_url='#')),
]
