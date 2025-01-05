from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
import django.shortcuts

from apps.materials.models import Material
from apps.materials.forms import MaterialForm


class Materials(FormView, ListView):
    template_name = "materials/main.html"
    form_class = MaterialForm
    model = Material
    context_object_name = "materials"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            context["materials"] = Material.objects.all()
        else:
            context["materials"] = Material.objects.filter(is_public=True)

        return context

    def form_valid(self, form):
        form.save()
        return django.shortcuts.redirect("materials:main")


class DeleteMaterialView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        if not request.user.is_staff:
            return django.shortcuts.redirect("materials:main")

        material = django.shortcuts.get_object_or_404(Material, pk=pk)
        material.delete()
        return django.shortcuts.redirect("materials:main")
