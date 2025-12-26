
from django.db import models
import uuid
from django.contrib.auth import get_user_model
from visitors.models import Visitor
User = get_user_model()
from django.utils import timezone
# =====================================================================
# Conversation Model
# =====================================================================
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name="conversations")
    status = models.BooleanField(default=True, verbose_name="Published")

    last_message = models.TextField(null=True, blank=True, verbose_name="Last Message")
    date_last_message = models.DateTimeField(null=True, blank=True, verbose_name="Date of Last Message")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ['-date_last_message']
    
    @classmethod
    def get_user_conversations(modelClass, user):
        return modelClass.objects.filter(user=user).order_by('-date_last_message')

    @classmethod
    def get_or_create_conversation(modelClass, user, visitor):
        conversation, created = modelClass.objects.get_or_create(
            user=user,
            visitor=visitor,
            status=True
        )
        return conversation, created

    def update_last_message(self, last_message):
        self.last_message = last_message[:150]  
        self.date_last_message = timezone.now()
        self.updated_at = timezone.now()
        self.save()

    def __str__(self):
        return f"Conversation between {self.user} and {self.visitor}"
# =====================================================================
# 
# 
# 
# =====================================================================
# Message Model
# =====================================================================
class Message(models.Model):
    SENDER_CHOICES = [('visitor', 'visitor'), ('user', 'user')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False, verbose_name="Read")
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES, verbose_name="Sender")
    visitor = models.ForeignKey(Visitor, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages', verbose_name="Visitor Sender")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages', verbose_name="User Sender")
    created_at = models.DateTimeField(auto_now_add=True)
     
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-created_at']

    def __str__(self):
        return f"Message: {self.conversation}"
# =====================================================================
# 
# 
# =====================================================================
# MessageImages Model
# =====================================================================
def image_message_upload_path(instance, filename):
    import os
    ext = os.path.splitext(filename)[1]  
    unique_filename = f"{uuid.uuid4()}{ext}"
    return f"chats/{instance.message.conversation.id}/images/{unique_filename}"

class MessageImages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=image_message_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "MessageImage"
        verbose_name_plural = "MessageImages"
        ordering = ['-created_at']

    def __str__(self):
        return f"Image: {self.message.id}"
# =====================================================================




