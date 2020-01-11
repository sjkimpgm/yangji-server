from rest_framework.pagination import CursorPagination, LimitOffsetPagination, PageNumberPagination


class GeneralCursorPagination(CursorPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    ordering = ('-created_at',)


class GeneralLimitOffsetPagination(LimitOffsetPagination):
    limit_query_param = 'page_size'
    offset_query_param = 'offset'


class GeneralPageNumberPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
