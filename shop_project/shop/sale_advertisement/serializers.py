from rest_framework.serializers import ModelSerializer

from sale_advertisement.models import SaleAdvertisement


class AllAdvertisementsSerializer(ModelSerializer):
    class Meta:
        model = SaleAdvertisement
        fields = ('id', 'advertisement_title', 'advertisement_price', 'publish_date',
                  'advertisement_location', 'is_new', 'views_amount')


class SingleAdvertisementSerializer(ModelSerializer):
    class Meta:
        model = SaleAdvertisement
        fields = '__all__'

    def save(self, **kwargs):
        self.validated_data['advertisement_location'] = (self.validated_data.get('advertisement_location')
                                                         .lower().capitalize())
        super().save()
