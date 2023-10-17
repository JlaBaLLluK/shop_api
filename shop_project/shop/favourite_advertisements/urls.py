from django.urls import path
from favourite_advertisements.views import *

urlpatterns = [
    path('favourite-advertisements/', AllFavouriteAdvertisementsView.as_view()),
]
