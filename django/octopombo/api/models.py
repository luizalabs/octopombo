from django.db import models


class Project(models.Model):
    channel = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    approved_label = models.CharField(max_length=100)

    class Meta(object):
        unique_together = ('channel', 'name')

    def __str__(self):
        return 'Channel: {channel}, project: {name}'.format(
            channel=self.channel,
            name=self.name
        )

    @classmethod
    def get_projects_by_channel(cls, channel_name):
        return cls.objects.filter(channel=channel_name)

    @classmethod
    def get_approved_label(cls, channel, name):
        return cls.objects.get(channel=channel, name=name).approved_label
