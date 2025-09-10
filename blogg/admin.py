from django.contrib import admin
from .models import Blog, Category, ProjectImage, ProjectView, Project, Tag

admin.site.register(Blog)
admin.site.register(Project)
admin.site.register(ProjectView)
admin.site.register(ProjectImage)
admin.site.register(Category)
admin.site.register(Tag)
