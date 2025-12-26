from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_experienceType(sender, **kwargs):
    if sender.name == 'experiences':
        from .models import ExperienceType
        ExperienceType.default_types()