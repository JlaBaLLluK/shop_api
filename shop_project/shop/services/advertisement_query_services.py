from django.core.exceptions import BadRequest
from django.db.models import QuerySet

from sale_advertisement.models import SaleAdvertisement


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
        self.price_lower_bound = ''
        self.price_upper_bound = ''

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
                self.is_new = bool(int(self.is_new))
        except ValueError:
            raise BadRequest

    def get_price_bounds(self):
        self.price_lower_bound = self.get_param_if_exists('price_lower_bound')
        self.price_upper_bound = self.get_param_if_exists('price_upper_bound')
        try:
            if self.price_lower_bound != '':
                self.price_lower_bound = int(self.price_lower_bound)
            else:
                self.price_lower_bound = 0

            if self.price_upper_bound != '':
                self.price_upper_bound = int(self.price_upper_bound)
            else:
                self.price_upper_bound = 99_999_999

        except ValueError:
            raise BadRequest

    def get_queryset_according_to_price(self):
        self.queryset = self.queryset.filter(advertisement_price__lte=self.price_upper_bound,
                                             advertisement_price__gte=self.price_lower_bound)

    def filter_queryset(self):
        if self.location != '':
            self.queryset = self.queryset.filter(advertisement_location=self.location)

        if self.is_new != '':
            self.queryset = self.queryset.filter(is_new=self.is_new)

    def sort_queryset(self):
        if self.sort_order != '':
            self.queryset = self.queryset.order_by(self.sort_queries[self.sort_order])

    def make_queryset(self):
        self.get_queryset_according_to_price()
        self.filter_queryset()
        self.sort_queryset()
        return self.queryset
