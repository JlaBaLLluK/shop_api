from django.contrib.auth.decorators import login_required
from django.urls import path
from authorization.views import *

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]
