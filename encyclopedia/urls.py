from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entryPage, name = "entryPage"),
    path("search/", views.search, name = "search"),
    path("create/", views.create_entry, name = "create"),
    path("edit/<str:entry_title>", views.edit_entry, name="edit"),
    path("random/", views.random_entry, name="random")
]