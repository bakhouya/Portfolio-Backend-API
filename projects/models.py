
from django.db import models
import uuid
from django.contrib.auth import get_user_model
from visitors.models import Visitor
User = get_user_model()
from skills.models import Skill

# ========================================================================
# ProjectType Model
# ========================================================================
class ProjectType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, verbose_name="Title", unique=True)
    status = models.BooleanField(default=True, verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Project Type"
        verbose_name_plural = "Project Types"
        ordering = ['created_at']

    def __str__(self):
        return self.title
# ========================================================================
# 
# 
# ========================================================================
# Project Model
# ========================================================================
class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    type = models.ForeignKey(ProjectType, on_delete=models.CASCADE, related_name="projects")

    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    details = models.TextField(verbose_name="Details")

    skills = models.ManyToManyField(Skill, blank=True, symmetrical=False, related_name='projects', verbose_name="Skills")
    likes = models.ManyToManyField(Visitor, blank=True, symmetrical=False, related_name='liked_projects', verbose_name="Likes")
    views = models.ManyToManyField(Visitor, blank=True, symmetrical=False, related_name='views_projects', verbose_name="Views")

    project_date = models.DateField(verbose_name="Project Date")
    demo_url = models.URLField(blank=True, null=True, verbose_name="Live Demo")
    github_url = models.URLField(blank=True, null=True, verbose_name="Github Url")
    video_url = models.URLField(blank=True, null=True, verbose_name="Video Url")

    status = models.BooleanField(default=False, verbose_name="Published")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
# ========================================================================
# 
# 
def project_image_upload_path(instance, filename):
    import os
    ext = os.path.splitext(filename)[1]  
    unique_filename = f"{uuid.uuid4()}{ext}"
    project_id = instance.project.id if instance.project else "unknown"
    return f"projects/{project_id}/{unique_filename}"
# ========================================================================
# ProjectImage Model
# ========================================================================
class ProjectImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images', verbose_name="Project")
    image = models.ImageField(upload_to=project_image_upload_path, verbose_name="Image")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"
        ordering = ['created_at']

    def __str__(self):
        return self.project.title
    

    def delete(self, *args, **kwargs):
        if self.image:
            import os
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
# ========================================================================




