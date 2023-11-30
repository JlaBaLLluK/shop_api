from django.utils.datetime_safe import datetime
from rest_framework.test import APITestCase
from rest_framework.status import *

from sale_advertisement.models import SaleAdvertisement
from sale_advertisement.serializers import AllAdvertisementsSerializer, SingleAdvertisementSerializer
from user.models import AuthUser


class GetAllAdvertisementsTests(APITestCase):
    url = '/api/sale_advertisement/'

    def setUp(self) -> None:
        author = AuthUser.objects.create_user(username='test_user1', password='test_user1_password')
        publish_date = datetime(year=2023, month=10, day=15, hour=12, minute=30, second=0)
        SaleAdvertisement.objects.create(advertisement_title="Chair", advertisement_description="Good wooden chair!",
                                         advertisement_location="Minsk", publish_date=publish_date,
                                         advertisement_price="10.00", is_new=True, advertisement_author=author
                                         )
        publish_date = datetime(year=2022, month=10, day=15, hour=12, minute=30, second=0)
        SaleAdvertisement.objects.create(advertisement_title="Table", advertisement_description="Good wooden table!",
                                         advertisement_location="Grodno", publish_date=publish_date,
                                         advertisement_price="20.00", is_new=True, advertisement_author=author
                                         )

    def test_if_get_unsorted_advertisements_successful(self):
        response = self.client.get(f"{self.url}{1}/")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(AllAdvertisementsSerializer(SaleAdvertisement.objects.all(), many=True).data, response.data)

    def test_if_get_newest_advertisements_successful(self):
        response = self.client.get(f"{self.url}{1}/?sort_order=newest")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            AllAdvertisementsSerializer(SaleAdvertisement.objects.order_by('-publish_date'), many=True).data,
            response.data)

    def test_if_get_sorted_most_cheep_advertisements_successful(self):
        response = self.client.get(f"{self.url}{1}/?sort_order=most_cheep")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            AllAdvertisementsSerializer(SaleAdvertisement.objects.order_by('advertisement_price'), many=True).data,
            response.data)

    def test_if_get_oldest_advertisements_successful(self):
        response = self.client.get(f"{self.url}{1}/?sort_order=oldest")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            AllAdvertisementsSerializer(SaleAdvertisement.objects.order_by('publish_date'), many=True).data,
            response.data)

    def test_if_get_sorted_most_expensive_advertisements_successful(self):
        response = self.client.get(f"{self.url}{1}/?sort_order=most_expensive")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            AllAdvertisementsSerializer(SaleAdvertisement.objects.order_by('-advertisement_price'), many=True).data,
            response.data)

    def test_if_get_data_unsuccessful_page_wrong(self):
        response = self.client.get(f"{self.url}{45}/")
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def test_if_get_data_unsuccessful_sort_order_wrong(self):
        response = self.client.get(f"{self.url}{45}/?sort_order=wrong_order")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)


class GetSingleAdvertisementTests(APITestCase):
    url = '/api/sale_advertisement/1/'

    def setUp(self) -> None:
        author = AuthUser.objects.create_user(username='test_user1', password='test_user1_password')
        publish_date = datetime(year=2023, month=10, day=15, hour=12, minute=30, second=0)
        SaleAdvertisement.objects.create(advertisement_title="Chair", advertisement_description="Good wooden chair!",
                                         advertisement_location="Minsk", publish_date=publish_date,
                                         advertisement_price="10.00", is_new=True, advertisement_author=author
                                         )

    def test_if_get_single_advertisement_successful(self):
        response = self.client.get(f"{self.url}{1}/")
        self.assertEqual(SingleAdvertisementSerializer(SaleAdvertisement.objects.get(pk=1)).data, response.data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_if_get_single_advertisement_unsuccessful(self):
        response = self.client.get(f"{self.url}{70}/")
        self.assertEqual(response.data["errors"], "This advertisement doesn't exist!")
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
