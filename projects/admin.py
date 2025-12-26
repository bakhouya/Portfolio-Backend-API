from django.contrib import admin
from .models import ProjectType, Project, ProjectImage

admin.site.register(ProjectType)
admin.site.register(Project)
admin.site.register(ProjectImage)
