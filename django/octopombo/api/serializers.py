from rest_framework import serializers

from octopombo.api.models import Project


class ProjectModelSerializer(serializers.ModelSerializer):

    name = serializers.CharField()
    channel = serializers.CharField()
    approved_label = serializers.CharField()

    class Meta:
        model = Project
        fields = (
            'name',
            'channel',
            'approved_label'
        )
