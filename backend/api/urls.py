from django.urls import path
from . import views

urlpatterns = [
    path("message/", views.QAListCreate.as_view(), name="note-list"),
    path("message/delete/<int:pk>", views.QADelete.as_view(), name="delete-note"),
]
