from django.db import models
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()

# ==================================================================================
# Profile Model
# ==================================================================================
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    job_title = models.CharField(blank=True, null=True, max_length=200, verbose_name="Job Title")
    bio = models.TextField(blank=True, null=True, verbose_name="Bio")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone")
    avatar = models.ImageField(upload_to='profile/avatars/', blank=True, null=True, verbose_name="Avatar")
    cv_file = models.FileField(upload_to='profile/files/', blank=True, null=True, verbose_name="Resumé CV")
    github_url = models.URLField(blank=True, null=True, verbose_name="GitHub")
    linkedin_url = models.URLField(blank=True, null=True, verbose_name="LinkedIn")
    youtube_url = models.URLField(blank=True, null=True, verbose_name="Youtube")
    facebook_url = models.URLField(blank=True, null=True, verbose_name="Facebook")
    instagram_url = models.URLField(blank=True, null=True, verbose_name="Instagram")
    whatsapp_url = models.URLField(blank=True, null=True, verbose_name="Whatsapp")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.user.username

    # =============================================================
    # Create default data Profile 
    # =============================================================
    @classmethod
    def default_profile(modelClass):
        if not modelClass.objects.exists():
            user = User.objects.first()
            if user is None:
                user = User.objects.create_user(
                    username='admin',
                    email='admin@example.com',
                    password='Admin123!',
                    first_name='Admin',
                    last_name='User',
                    is_staff=True,
                    is_superuser=True
                )          

            modelClass.objects.create(
                user= user,
                job_title= "Full Stack Developer",
                bio= "Passionate developer specializing in Django, React, and modern web technologies.",
                phone= "+212772013984",
                github_url= "https://github.com/bakhouya",
                linkedin_url=  "https://linkedin.com/in/bakhouya",
                youtube_url= "",
                facebook_url= "",
                instagram_url= "",
                whatsapp_url= "https://wa.me/212772013984",

                avatar= None, 
                cv_file= None 
            )       
            return True
        return False
    # =============================================================

# ==================================================================================


# ==================================================================================
# About Section Model 
# ==================================================================================
class About(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="About", verbose_name="User")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    image = models.ImageField(upload_to='profile/about/', blank=True, null=True, verbose_name="Image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Sections"

    def __str__(self):
        return self.title
# ==================================================================================
