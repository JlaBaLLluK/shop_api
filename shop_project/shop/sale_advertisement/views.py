from django.core.exceptions import BadRequest
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import *
from sale_advertisement.serializers import *
from rest_framework.views import APIView
from sale_advertisement.models import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from services.advertisement_query_services import AdvertisementQueryServices


class AllAdvertisementsView(APIView):
    serializer_class = AllAdvertisementsSerializer
    MAX_ADVERTISEMENTS_ON_PAGE = 20

    def get(self, request, page_number):
        advertisement_query_services = AdvertisementQueryServices(request, SaleAdvertisement.objects.all())
        try:
            advertisement_query_services.get_sort_order()
            advertisement_query_services.get_filters()
        except BadRequest:
            return Response({"errors": "Wrong query!"})

        try:
            advertisement_query_services.filter_queryset()
            advertisement_query_services.sort_queryset()
        except BadRequest:
            return Response({"error": "Unknown query!"}, status=HTTP_400_BAD_REQUEST)

        advertisements = advertisement_query_services.queryset[(page_number - 1) * self.MAX_ADVERTISEMENTS_ON_PAGE:
                                                               page_number * self.MAX_ADVERTISEMENTS_ON_PAGE]
        if len(advertisements) == 0:
            return Response({"information": "There is no data yet!"}, status=HTTP_204_NO_CONTENT)

        serializer = AllAdvertisementsSerializer(advertisements, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class CreateAdvertisementView(APIView):
    serializer_class = SingleAdvertisementSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        serializer = SingleAdvertisementSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        serializer.create(serializer.validated_data)
        return Response(serializer.data, status=HTTP_201_CREATED)


class SingleAdvertisementView(APIView):
    serializer_class = SingleAdvertisementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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

        users_checked_advertisement = advertisement.users_checked_advertisement.all()
        if request.user.is_authenticated and request.user not in users_checked_advertisement:
            advertisement.views_amount += 1
            advertisement.save()
            advertisement.users_checked_advertisement.add(request.user)

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
