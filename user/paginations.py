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

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "data": schema,
                "meta": {
                    "type": "object",
                    "properties": {
                        "pagination": {
                            "type": "object",
                            "properties": {
                                "total": {
                                    "type": "integer",
                                    "example": 0
                                },
                                "page": {
                                    "type": "integer",
                                    "example": 0
                                },
                                "size": {
                                    "type": "integer",
                                    "example": 0
                                }
                            }
                        }
                    }
                }
            }
        }


class CustomAdminPagination(PageNumberPagination):
    page_size_query_param = "size"
    
    def get_paginated_response(self, data):
        return Response({
            "data": data,
            "meta": {
                "pagination": {
                    "total": self.page.paginator.num_pages,
                    "page": self.page.number,
                    "size": self.get_page_size(self.request),
                },
                "hint": {
                    "city": data.city
                }
            }
        })

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "data": schema,
                "meta": {
                    "type": "object",
                    "properties": {
                        "pagination": {
                            "type": "object",
                            "properties": {
                                "total": {
                                    "type": "integer",
                                    "example": 0
                                },
                                "page": {
                                    "type": "integer",
                                    "example": 0
                                },
                                "size": {
                                    "type": "integer",
                                    "example": 0
                                }
                            }
                        },
                        "hint": {
                            "type": "object",
                            "properties": {
                                "city": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "id": {
                                                "type": "integer",
                                                "example": 0
                                            },
                                            "name": {
                                                "type": "string",
                                                "example": "string"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }