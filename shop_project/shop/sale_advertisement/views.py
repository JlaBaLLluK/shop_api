from django.http import Http404
from django.shortcuts import get_object_or_404
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


class CreateAdvertisementView(APIView):
    serializer_class = SingleAdvertisementSerializer

    @staticmethod
    def post(request):
        serializer = SingleAdvertisementSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        serializer.create(serializer.validated_data)
        return Response(serializer.data, status=HTTP_201_CREATED)


class SingleAdvertisementView(APIView):
    serializer_class = SingleAdvertisementSerializer

    @staticmethod
    def get_advertisement(pk):
        try:
            advertisement = get_object_or_404(SaleAdvertisement, pk=pk)
        except Http404:
            return None

        return advertisement

    def get(self, request, page_number, pk):
        advertisement = self.get_advertisement(pk)
        if advertisement is None:
            return Response({"errors": "This advertisement doesn't exist!"}, status=HTTP_404_NOT_FOUND)

        return Response(SingleAdvertisementSerializer(advertisement).data, status=HTTP_200_OK)

    def put(self, request, page_number, pk):
        advertisement = self.get_advertisement(pk)
        if advertisement is None:
            return Response({"errors": "This advertisement doesn't exist!"}, status=HTTP_404_NOT_FOUND)

        serializer = SingleAdvertisementSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        serializer.update(advertisement, serializer.validated_data)
        return Response(serializer.data, status=HTTP_200_OK)

    def delete(self, request, page_number, pk):
        advertisement = self.get_advertisement(pk)
        if advertisement is None:
            return Response({"errors": "This advertisement doesn't exist!"}, status=HTTP_404_NOT_FOUND)

        advertisement.delete()
        return Response({"success": "Advertisement was deleted successfully!"}, status=HTTP_200_OK)
