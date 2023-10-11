from rest_framework.serializers import ModelSerializer

from sale_advertisement.models import SaleAdvertisement


class AllAdvertisementsSerializer(ModelSerializer):
    class Meta:
        model = SaleAdvertisement
        fields = ('advertisement_title', 'advertisement_price', 'currency', 'publish_date',
                  'advertisement_location', 'is_new', 'views_amount')


class SingleAdvertisementSerializer(ModelSerializer):
    class Meta:
        model = SaleAdvertisement
        fields = '__all__'
