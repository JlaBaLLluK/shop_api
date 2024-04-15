from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404
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
        advertisements = FavouriteAdvertisements.objects.filter(user=request.user)
        if len(advertisements) == 0:
            return Response({"information": "There is no data yet!"}, status=HTTP_204_NO_CONTENT)

        serializer = AllFavouriteAdvertisementsSerializer(advertisements, many=True)
        return Response(serializer.data)


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
            advertisement_in_favourite = FavouriteAdvertisements.objects.get(advertisement=advertisement, user=request.user)
        except ObjectDoesNotExist:
            favourite_advertisement = FavouriteAdvertisements(user=request.user, advertisement=advertisement)
            favourite_advertisement.save()
            return Response({"success": "Advertisement was added to favourite successfully!"}, status=HTTP_200_OK)
        else:
            FavouriteAdvertisements.objects.get(pk=advertisement_in_favourite.pk).delete()
            return Response({"success": "This advertisement was removed from favourite!"},
                            status=HTTP_204_NO_CONTENT)
