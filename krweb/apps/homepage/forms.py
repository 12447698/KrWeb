from django import forms


class ProjectForm(forms.Form):
    project = forms.CharField(
        label="Код проекта",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Введите код проекта"}),
    )
