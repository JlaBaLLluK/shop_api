from django.core.exceptions import BadRequest
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

    def get_sorted_advertisements(self, page_number, sort_order):
        advertisements = SaleAdvertisement.objects.all()
        slice_lower_bound = (page_number - 1) * self.MAX_ADVERTISEMENTS_ON_PAGE
        slice_upper_bound = self.MAX_ADVERTISEMENTS_ON_PAGE * page_number
        if sort_order == 'newest':
            advertisements = advertisements.order_by('-publish_date').values()
        elif sort_order == 'oldest':
            advertisements = advertisements.order_by('publish_date').values()
        elif sort_order == 'most_popular':
            advertisements = advertisements.order_by('-views_amount').values()
        elif sort_order == 'most_unpopular':
            advertisements = advertisements.order_by('views_amount').values()
        elif sort_order is None:
            pass
        else:
            raise BadRequest

        return advertisements[slice_lower_bound:slice_upper_bound]

    def get(self, request, page_number):
        sort_order = request.query_params.get('sort_order')
        try:
            advertisements = self.get_sorted_advertisements(page_number, sort_order)
        except BadRequest:
            return Response({"error": "Unknown sort order!"}, status=HTTP_400_BAD_REQUEST)
        if len(advertisements) == 0:
            return Response({"information": "There is no data yet!"}, status=HTTP_204_NO_CONTENT)

        serializer = AllAdvertisementsSerializer(advertisements, many=True)
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

        advertisement.views_amount += 1
        advertisement.save()
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
