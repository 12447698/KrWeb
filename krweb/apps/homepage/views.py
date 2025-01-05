import django.views.generic
import django.shortcuts

from apps.homepage.forms import ProjectForm
from apps.projects.models import Project


class Home(django.views.generic.View):
    def get(self, request, *args, **kwargs):
        form = ProjectForm()
        return django.shortcuts.render(
            request,
            "homepage/main.html",
            {
                "form": form,
            },
        )

    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            project_code = form.cleaned_data["project"]
            try:
                project = Project.objects.get(code=project_code)
            except Project.DoesNotExist:
                project = None

            return django.shortcuts.render(
                request,
                "projects/project_page.html",
                {
                    "project": project,
                },
            )
