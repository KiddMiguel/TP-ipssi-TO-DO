from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("liste/", views.liste, name="liste"),
    path("liste_active/", views.liste_active, name="liste_active"),
    path("detail/<int:id>/", views.detail, name="detail"),
]