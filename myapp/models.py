from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

#追記
from django.utils import timezone
import uuid

class CustomUser(AbstractUser):
    image = models.ImageField()#保存様式画像
    def __str__(self):
        return self.username
    
# class Room(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     name = models.CharField(max_length=50)
#     created_at = models.DateTimeField(default=timezone.now)

    
class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # room = models.ForeignKey(
    #     # Room,
    #     blank=True,
    #     null=True,
    #     related_name='room_meesages',
    #     on_delete=models.CASCADE
    # )
    # name = models.CharField(max_length=50)
    
    sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="sender")
    recipient=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="recipient")
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    # sender = models.IntegerField(null=False, blank=True)
    # recipient = models.IntegerField(null=False, blank=True)

