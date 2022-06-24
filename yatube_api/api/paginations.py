from rest_framework.pagination import LimitOffsetPagination


class StandardResultSetPagination(LimitOffsetPagination):
    page_size = 5
    page_size_query_param = 'page_size'