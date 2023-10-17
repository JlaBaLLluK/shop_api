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

    def get_param_if_exists(self, param):
        value = self.request.query_params.get(param)
        return value if value is not None else ''

    def get_sort_order(self):
        self.sort_order = self.get_param_if_exists('sort_order')
        if self.sort_order != '' and self.sort_order not in self.sort_queries.keys():
            raise BadRequest

    def get_filters(self):
        self.location = self.get_param_if_exists('location')
        try:
            self.is_new = self.get_param_if_exists('is_new')
            if self.is_new != '':
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
