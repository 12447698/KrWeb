from django import forms

from apps.materials.models import Material


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ("name", "file", "is_public")

    is_public = forms.BooleanField(required=False, label="Публичный материал")
