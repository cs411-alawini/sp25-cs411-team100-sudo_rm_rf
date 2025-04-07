from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.searchbox),
    path("<int:aui>/results/", views.result),
]