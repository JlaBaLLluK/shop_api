from django.urls import path
from sale_advertisement.views import *

urlpatterns = [
    path('<int:page_number>/', AllAdvertisementsView.as_view()),
    path('create-advertisement/', CreateAdvertisementView.as_view()),
    path('<int:page_number>/<int:pk>/', SingleAdvertisementView.as_view()),
]
