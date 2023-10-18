from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.datetime_safe import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from favourite_advertisements.serializers import *


class AllFavouriteAdvertisementsView(APIView):
    serializer_class = AllFavouriteAdvertisementsSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        advertisements = FavouriteAdvertisements.objects.all()
        if len(advertisements) == 0:
            return Response({"information": "There is no data yet!"}, status=HTTP_204_NO_CONTENT)

        serializer = AllFavouriteAdvertisementsSerializer(advertisements, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class AddToFavouriteAdvertisementsView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_advertisement(pk):
        try:
            advertisement = get_object_or_404(SaleAdvertisement, pk=pk)
        except Http404:
            return None

        return advertisement

    def post(self, request, page_number, pk):
        advertisement = self.get_advertisement(pk)
        if advertisement is None:
            return Response({"errors": "This advertisements doesn't exist!"}, status=HTTP_404_NOT_FOUND)

        try:
            FavouriteAdvertisements.objects.get(advertisement=advertisement)
        except ObjectDoesNotExist:
            favourite_advertisement = FavouriteAdvertisements(user=request.user, advertisement=advertisement)
            favourite_advertisement.save()
            return Response({"success": "Advertisement was added to favourite successfully!"}, status=HTTP_200_OK)
        else:
            return Response({"success": "This advertisement already in favourite advertisements!"},
                            status=HTTP_204_NO_CONTENT)
