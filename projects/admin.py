from projects.models import Project, RequiredProjectFile, UploadedProjectFile
from django.contrib import admin

# Register your models here.

class UploadedProjectFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'project', 'file_name', 'uploaded_by']

class UploadedProjectFileInline(admin.TabularInline):
    model = UploadedProjectFile
    extra = 0

class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['title']
    sortable_by = ['title']
    prepopulated_fields = {'user_friendly_url': ('title',)}
    inlines = [UploadedProjectFileInline]

class RequiredProjectFileAdmin(admin.ModelAdmin):
    inlines = [UploadedProjectFileInline]

admin.site.register(Project, ProjectAdmin)
admin.site.register(RequiredProjectFile, RequiredProjectFileAdmin)
admin.site.register(UploadedProjectFile, UploadedProjectFileAdmin)