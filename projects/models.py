from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextUploadingField()
    allocated_to = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self) -> str:
        return self.title