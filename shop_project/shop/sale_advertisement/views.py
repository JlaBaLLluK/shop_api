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

    @staticmethod
    def get_sort_order(request):
        return request.query_params.get('sort_order')

    @staticmethod
    def get_filters(request):
        location = request.query_params.get('location')
        is_new = request.query_params.get('is_new')
        return [location if location is not None else None] + [bool(int(is_new)) if is_new is not None else None]

    def get_sorted_advertisements(self, page_number, sort_order, advertisements):
        queries = {
            "newest": "-publish_date",
            "oldest": "publish_date",
            "most_popular": "-views_amount",
            "most_unpopular": "views_amount",
            "most_cheep": "advertisement_price",
            "most_expensive": "-advertisement_price",
        }

        if sort_order not in queries.keys() and sort_order is not None:
            raise BadRequest
        elif sort_order is not None:
            advertisements = advertisements.order_by(queries[sort_order])

        slice_lower_bound = (page_number - 1) * self.MAX_ADVERTISEMENTS_ON_PAGE
        slice_upper_bound = self.MAX_ADVERTISEMENTS_ON_PAGE * page_number
        return advertisements[slice_lower_bound:slice_upper_bound]

    @staticmethod
    def get_filtered_advertisements(filters):
        advertisements = SaleAdvertisement.objects.all()
        if filters[0] is not None:
            advertisements = advertisements.filter(advertisement_location=filters[0])

        if filters[1] is not None:
            advertisements = advertisements.filter(is_new=filters[1])

        return advertisements

    def get(self, request, page_number):
        sort_order = self.get_sort_order(request)
        filters = self.get_filters(request)
        filtered_advertisements = self.get_filtered_advertisements(filters)
        try:
            advertisements = self.get_sorted_advertisements(page_number, sort_order, filtered_advertisements)
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
