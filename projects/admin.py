from projects.models import Project
from django.contrib import admin

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['title']
    sortable_by = ['title']

admin.site.register(Project, ProjectAdmin)