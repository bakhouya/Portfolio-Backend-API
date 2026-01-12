
from django.db import models
import uuid

# =====================================================================
# Contact Model
# =====================================================================
class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    status = models.BooleanField(default=False, verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ['-created_at']


    def __str__(self):
        return self.title
# =====================================================================






