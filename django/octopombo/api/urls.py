from django.contrib import admin
from django.urls import path

from octopombo.api import views


urlpatterns = [
    path(
        'projects',
        views.ProjectViewSet.as_view({'get': 'list','post': 'create'}),
        name='api'
    ),
    path('pulls', views.PullRequestsViewSet.as_view(), name='pulls')
]
