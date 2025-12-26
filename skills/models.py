from django.db import models
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()


# ===================================================================================
# ===================================================================================
class CategorySkill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, verbose_name="Title", unique=True)
    status = models.BooleanField(default=True, verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category Skills"
        verbose_name_plural = "Categories Skills"
        ordering = ['created_at']

    def __str__(self):
        return self.title
# ===================================================================================
# 
# 
# 
# ===================================================================================
# ===================================================================================
class Skill(models.Model):
    SKILL_LEVEL_CHOICES = [
        ('beginner', 'Beginner'), ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'), ('expert', 'Expert'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skills")
    title = models.CharField(max_length=100, verbose_name="Title", unique=True)
    category = models.ForeignKey(CategorySkill, on_delete=models.CASCADE, related_name='skills', verbose_name="Category")
    level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES, verbose_name="Level")
    percentage = models.PositiveIntegerField(verbose_name="Percentage", help_text="0 to 100")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="Icon")
    color = models.CharField(max_length=7, default='#4A90E2', verbose_name="Color")
    status = models.BooleanField(default=True, verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        ordering = ['created_at']

    def __str__(self):
        return self.title
# ===================================================================================


