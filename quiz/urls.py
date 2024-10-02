from django.urls import path
from . import views

urlpatterns = [
    path("", views.welcome_page),
    path("list", views.list_words),
    path("quiz", views.quiz),
    path("settings", views.settings),
    path("prepare_quiz", views.prepare_quiz),
]
