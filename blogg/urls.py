from django.urls import path
from .views import project_detail

urlpatterns = [
    path("project-detail/<slug:slug>/", project_detail, name="project_detail"),
]
