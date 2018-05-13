from rest_framework import pagination


class PullRequestPagination(pagination.PageNumberPagination):
    page_size = 10000
