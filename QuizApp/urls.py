from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('quiz/<str:url>', views.view_quiz, name="view_quiz"),
    path('quiz/<str:url>/start', views.start_quiz, name="start_quiz"),
]
