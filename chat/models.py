from django.db import models

from account.models import Account
# Create your models here.

class Chat(models.Model):
	"""Messaging chat model"""
	members = models.ManyToManyField(Account, blank=True, related_name='chats')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.id)


class Message(models.Model):
	"""The message sending by account"""
	user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='messages')
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_messages')
	message = models.TextField()
	files = models.FileField(upload_to='media/chat/', null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'Message "{self.message[:20]}..." by {self.user} in chat "{str(self.chat.id)}".'