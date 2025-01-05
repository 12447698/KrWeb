from django.contrib import admin

from apps.materials.models import Material


class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "uploaded_at", "is_public")
    search_fields = ("name",)
    list_filter = ("is_public", "uploaded_at")
    ordering = ("-uploaded_at",)


admin.site.register(Material, MaterialAdmin)
