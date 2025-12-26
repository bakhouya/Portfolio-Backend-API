from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_educationsType(sender, **kwargs):
    if sender.name == 'educations':
        from .models import Profile
        Profile.default_profile()