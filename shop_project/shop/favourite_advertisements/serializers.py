from rest_framework.serializers import ModelSerializer
from favourite_advertisements.models import *


class AllFavouriteAdvertisementsSerializer(ModelSerializer):
    class Meta:
        model = FavouriteAdvertisements
        fields = "__all__"
