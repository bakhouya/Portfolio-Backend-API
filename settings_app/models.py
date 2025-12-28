
import uuid
from django.db import models


# ============================================================================================
# PlatformSettings Model:
# This form is used to store basic platform settings such as title, description, logos, icons
# It should contain only one record in the database.
# ============================================================================================
class PlatformSettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    dark_logo = models.ImageField(upload_to="settings/platform/", blank=True, null=True, verbose_name="Dark Logo")
    light_logo = models.ImageField(upload_to="settings/platform/", blank=True, null=True, verbose_name="Light Logo")
    favicon = models.ImageField(upload_to="settings/platform/", blank=True, null=True)
    
    contact_email = models.EmailField(blank=True, null=True, verbose_name="Contact Email")
    support_email = models.EmailField(blank=True, null=True, verbose_name="Support Email")
    phone = models.CharField(max_length=20, blank=True, null=True)  
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Platform Settings"
        verbose_name_plural = "Platform Settings"

    def __str__(self):
        return f"{self.title} - Settings"
    
    # ======================================================================================
    # This function ensures that only one record is saved in the database.
    # If there are pre-existing settings, it prevents the creation of a new record 
    # updates the existing record instead of adding a new one.
    # ======================================================================================
    def save(self, *args, **kwargs):
        if PlatformSettings.objects.exists() and not self.pk:
            settings = PlatformSettings.objects.first()
            self.id = settings.id
            self.pk = settings.pk
        super().save(*args, **kwargs)
    # ======================================================================================

    # ======================================================================================
    # This function returns the existing platform settings,
    # and if none exist, it automatically creates a new record with default settings.
    # ======================================================================================
    @classmethod
    def get_settings(classObject):
        if classObject.objects.exists():
            return classObject.objects.first()
        else:
            return classObject.objects.create(
                title='Personal Portfolio',
                description='A platform for biulding Personel Portfolio.',
                contact_email='kamfour1997@gmail.com',
                support_email='kamfour1997@gmail.com',
                phone='0772013984'
            )
    # ====================================================================================== 
# ============================================================================================
# End Platform Settings Model
# ============================================================================================
# 
# 
# 
# ============================================================================================
# Content Model ( actice section option and data any section)
# ============================================================================================
class Content(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hero = models.BooleanField(default=True)
    about = models.BooleanField(default=True)
    about_title = models.CharField(max_length=255)
    about_description = models.TextField(blank=True, null=True)

    skills = models.BooleanField(default=True)
    skill_title = models.CharField(max_length=255)
    skill_description = models.TextField(blank=True, null=True)

    project = models.BooleanField(default=True)
    project_title = models.CharField(max_length=255)
    project_description = models.TextField(blank=True, null=True)

    experience = models.BooleanField(default=True)
    experience_title = models.CharField(max_length=255)
    experience_description = models.TextField(blank=True, null=True)

    education = models.BooleanField(default=True)
    education_title = models.CharField(max_length=255)
    education_description = models.TextField(blank=True, null=True)

    certificate = models.BooleanField(default=True)
    certificate_title = models.CharField(max_length=255)
    certificate_description = models.TextField(blank=True, null=True)

    service = models.BooleanField(default=True)
    service_title = models.CharField(max_length=255)
    service_description = models.TextField(blank=True, null=True)

    contact = models.BooleanField(default=True)
    contact_title = models.CharField(max_length=255)
    contact_description = models.TextField(blank=True, null=True)

    faq = models.BooleanField(default=True)
    faq_title = models.CharField(max_length=255)
    faq_description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Content"
        verbose_name_plural = "Contents"

    def __str__(self):
        return f"{self.id} - Content"

    # ======================================================================================
    def save(self, *args, **kwargs):
        if Content.objects.exists() and not self.pk:
            settings = Content.objects.first()
            self.id = settings.id
            self.pk = settings.pk
        super().save(*args, **kwargs)

    # ======================================================================================
    @classmethod
    def get_content(classObject):
        if classObject.objects.exists():
            return classObject.objects.first()
        else:
            return classObject.objects.create(
                hero = True,
                about = True,
                about_title = "About",
                about_description = "Description About",

                skills = True,
                skill_title = "skill",
                skill_description = "Description skill",

                project = True,
                project_title = "project",
                project_description = "Description project",

                experience = True,
                experience_title = "experience",
                experience_description = "Description experience",

                education = True,
                education_title = "education",
                education_description = "Description education",

                certificate = True,
                certificate_title = "certifical",
                certificate_description = "Description certifical",

                service = True,
                service_title = "service",
                service_description = "Description service",

                contact = True,
                contact_title = "contact",
                contact_description = "Description contact",

                faq = True,
                faq_title = "faq",
                faq_description = "Description faq"
            )
    # ====================================================================================== 
    # ======================================================================================
# ============================================================================================
# 
# 
# 
# ============================================================================================
# Faq Model (Quiestion = title, Answer = description)
# ============================================================================================
class Faq(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Faq"
        verbose_name_plural = "Faqs"

    def __str__(self):
        return self.title
# ============================================================================================




