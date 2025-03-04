# Generated by Django 4.2.16 on 2025-01-05 16:09

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Название проекта"),
                ),
                (
                    "code",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="Код проекта"
                    ),
                ),
                (
                    "html_content",
                    ckeditor.fields.RichTextField(verbose_name="HTML контент проекта"),
                ),
            ],
        ),
    ]
