import sys

from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request


class CustomPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'

    def get_page_size(self, request: Request) -> int:
        if request.query_params.get(self.page_size_query_param) == 'all':
            return sys.maxsize
        else:
            return super().get_page_size(request)
