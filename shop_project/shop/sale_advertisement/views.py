from rest_framework.response import Response
from rest_framework.status import *
from sale_advertisement.serializers import *
from rest_framework.views import APIView
from sale_advertisement.models import *


class AllAdvertisementsView(APIView):
    serializer_class = AllAdvertisementsSerializer
    MAX_ADVERTISEMENTS_ON_PAGE = 20

    def get(self, request, page_number):
        goods = SaleAdvertisement.objects.all()[
                (page_number - 1) * self.MAX_ADVERTISEMENTS_ON_PAGE: self.MAX_ADVERTISEMENTS_ON_PAGE * page_number]
        if len(goods) == 0:
            return Response({"information": "There is no data yet!"}, status=HTTP_204_NO_CONTENT)

        serializer = AllAdvertisementsSerializer(goods, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class SingleAdvertisementView(APIView):
    serializer_class = SingleAdvertisementSerializer

    @staticmethod
    def get(request, page_number, pk):
        pass
