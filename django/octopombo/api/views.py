import json

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from octopombo.api.handler import GithubProject
from octopombo.api.models import Project
from octopombo.api.pagination import PullRequestPagination
from octopombo.api.serializers import ProjectModelSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer


class PullRequestsViewSet(APIView):

    def get(self, request):
        project = GithubProject(request.GET.get('channel'))
        prs = project.get_pull_requests()
        pulls = {
            'pulls': [pr._asdict() for pr in prs]
        }
        return Response(pulls, status=status.HTTP_200_OK)
