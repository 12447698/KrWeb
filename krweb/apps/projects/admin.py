from django.contrib import admin

from apps.projects.models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "html_content",
    )
    search_fields = (
        "name",
        "code",
    )
    list_filter = ("name",)
    ordering = ("name",)


admin.site.register(Project, ProjectAdmin)
