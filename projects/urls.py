from django.urls import path
from . import views

urlpatterns = [
    path('<str:url>', views.view, name="view_project"),
]
