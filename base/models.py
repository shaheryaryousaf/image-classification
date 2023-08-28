from django.db import models


class Images(models.Model):
    image = models.ImageField(
        upload_to='profiles/%Y/%M/%D/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Images'
