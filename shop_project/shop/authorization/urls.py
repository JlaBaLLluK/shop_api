from django.contrib.auth.decorators import login_required
from django.urls import path
from authorization.views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', login_required(LogoutView.as_view(), login_url='login')),
]
