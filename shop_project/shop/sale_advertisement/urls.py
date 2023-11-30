from django.urls import path

from favourite_advertisements.views import AddToFavouriteAdvertisementsView
from sale_advertisement.views import *

urlpatterns = [
    path('<int:page_number>/', AllAdvertisementsView.as_view()),
    path('create-advertisement/', CreateAdvertisementView.as_view()),
    path('<int:page_number>/<int:pk>/', SingleAdvertisementView.as_view()),
    path('<int:page_number>/<int:pk>/add-to-favourite/', AddToFavouriteAdvertisementsView.as_view()),
]
