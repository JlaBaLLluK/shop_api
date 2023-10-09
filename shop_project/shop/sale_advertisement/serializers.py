from rest_framework.serializers import ModelSerializer

from sale_advertisement.models import SaleAdvertisement


class AllAdvertisementsSerializer(ModelSerializer):
    class Meta:
        model = SaleAdvertisement
        fields = ('advertisement_title', 'publish_date', 'advertisement_price', 'currency', 'advertisement_location')


class SingleAdvertisementSerializer(ModelSerializer):
    class Meta:
        model = SaleAdvertisement
        fields = '__all__'
