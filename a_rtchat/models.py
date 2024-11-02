from django.db import models
from django.contrib.auth.models import User
import shortuuid

# Create your models here.

class ChatGroup(models.Model):
    group_name = models.CharField(max_length=100,unique=True,default=shortuuid.uuid)
    users_online = models.ManyToManyField(User,related_name='online_in_groups',blank=True)
    members = models.ManyToManyField(User,related_name='chat_groups',blank=True)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.group_name

class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup,related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author.username} : {self.body[:20]}'
    
    class Meta:
        ordering = ['-created_at']

class Reviews(models.Model):
    name = models.CharField(max_length=100)
    review = models.CharField(max_length=1000)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} : {self.review[:20]}'
    
    class Meta:
        ordering = ['-created_at']