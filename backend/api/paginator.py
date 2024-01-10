from rest_framework import pagination


class CustomPaginator(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'


class CartPaginator(pagination.LimitOffsetPagination):
    max_limit = 100
    page_size_query_param = 'limit'
