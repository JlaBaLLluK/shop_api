from django.urls import path
from sale_advertisement.views import *

urlpatterns = [
    path('<int:page_number>/', AllAdvertisementsView.as_view()),
]
