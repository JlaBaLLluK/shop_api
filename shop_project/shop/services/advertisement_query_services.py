from django.core.exceptions import BadRequest
from django.db.models import QuerySet


class AdvertisementQueryServices:
    sort_queries = {
        "newest": "-publish_date",
        "oldest": "publish_date",
        "most_popular": "-views_amount",
        "most_unpopular": "views_amount",
        "most_cheep": "advertisement_price",
        "most_expensive": "-advertisement_price",
    }

    def __init__(self, request, queryset: QuerySet):
        self.request = request
        self.queryset = queryset
        self.sort_order = ''
        self.is_new = ''
        self.location = ''

    def get_sort_order(self):
        if self.request.query_params.get('sort_order') is not None:
            self.sort_order = self.request.query_params.get('sort_order')
        if self.sort_order != '' and self.sort_order not in self.sort_queries.keys():
            raise BadRequest

    def get_filters(self):
        if self.request.query_params.get('location') is not None:
            self.location = self.request.query_params.get('location')
        try:
            if self.request.query_params.get('is_new') is not None:
                self.is_new = bool(int(self.request.query_params.get('is_new')))
        except ValueError:
            raise BadRequest

    def filter_queryset(self):
        if self.location != '':
            self.queryset = self.queryset.filter(advertisement_location=self.location)

        if self.is_new != '':
            self.queryset = self.queryset.filter(is_new=self.is_new)

    def sort_queryset(self):
        if self.sort_order != '':
            self.queryset = self.queryset.order_by(self.sort_queries[self.sort_order])
