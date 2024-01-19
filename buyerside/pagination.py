from rest_framework.pagination import PageNumberPagination


class Carlistpagination(PageNumberPagination):
    page_size = 7
    page_query_param = "page"
    page_size_query_param = "size"
    max_page_size = 10
