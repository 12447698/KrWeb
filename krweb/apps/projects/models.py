from django.db import models
from ckeditor.fields import RichTextField


class Project(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название проекта",
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Код проекта",
    )
    html_content = RichTextField(
        verbose_name="HTML контент проекта",
    )

    def __str__(self):
        return self.name
