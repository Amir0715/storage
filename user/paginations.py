from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size_query_param = "size"

    def get_paginated_response(self, data):
        return Response({
            "data": data,
            "meta": {
                "pagination": {
                    "total": self.page.paginator.num_pages,
                    "page": self.page.number,
                    "size": self.get_page_size(self.request),
                }
            }
        })