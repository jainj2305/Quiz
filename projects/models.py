from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextUploadingField()
    allocated_to = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    user_friendly_url = models.SlugField(null=False, blank=False, unique=True)

    def __str__(self) -> str:
        return self.title

class RequiredProjectFile(models.Model):
    file_name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.file_name

class UploadedProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file_name = models.ForeignKey(RequiredProjectFile, on_delete=models.CASCADE)
    file = models.FileField()
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.project.title + " -> " + self.file_name.file_name