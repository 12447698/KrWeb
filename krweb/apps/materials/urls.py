from django.urls import path

import apps.materials.views

app_name = "materials"
urlpatterns = [
    path("", apps.materials.views.Materials.as_view(), name="main"),
    path(
        "delete/<int:pk>/",
        apps.materials.views.DeleteMaterialView.as_view(),
        name="delete",
    ),
]
