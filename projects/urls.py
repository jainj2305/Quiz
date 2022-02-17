from django.urls import path
from . import views

urlpatterns = [
    path('<str:url>', views.view, name="view_project"),
    path('<str:url>/<str:file_name>/upload', views.upload_project_files, name="upload_project_files")
]
