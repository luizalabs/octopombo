from django.contrib import admin

from octopombo.api.models import Project


@admin.register(Project)
class OrderAdmin(admin.ModelAdmin):
    pass
