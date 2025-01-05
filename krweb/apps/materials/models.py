from django.db import models


class Material(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название",
    )
    file = models.FileField(
        upload_to="materials/",
        verbose_name="Файл",
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата загрузки",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Публичный",
    )

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"

    def __str__(self):
        return self.name
