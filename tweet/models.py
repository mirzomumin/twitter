from django.db import models
from django.utils import timezone

from account.models import Account
# Create your models here.

class Tweet(models.Model):
	"""Simple tweet model"""
	account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='tweets')
	text = models.TextField()
	media = models.FileField(upload_to='media', null=True, blank=True)
	liked_by = models.ManyToManyField(Account, blank=True, related_name='liked_tweets')
	retweeted_by = models.ManyToManyField(Account, blank=True, related_name='retweeted_tweets')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'"{self.text[:50]}" tweeted by {self.account.username}'


class Comment(models.Model):
	"""Comment of related tweet"""
	account = models.ForeignKey(Account, on_delete=models.CASCADE)
	tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments')
	parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
	text = models.TextField()
	media = models.FileField(upload_to='media', null=True, blank=True)
	liked_by = models.ManyToManyField(Account, blank=True, related_name='liked_comments')
	retweeted_by = models.ManyToManyField(Account, blank=True, related_name='retweeted_comments')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'"{self.text[:50]}" left by {self.account.username}'


class Notification(models.Model):
	NOTIFICATION_TYPES = (
		('like', 'Like'),
		('comment', 'Comment'),
		('follow', 'Follow'),
		('retweet', 'Retweet'),
	)
	notification_type = models.CharField(
		max_length=7,
		null=True, blank=True,
		choices=NOTIFICATION_TYPES)
	to_user = models.ForeignKey(Account,
		related_name='notification_to',
		on_delete=models.CASCADE, null=True)
	from_user = models.ForeignKey(Account,
		related_name='notification_from',
		on_delete=models.CASCADE, null=True)
	tweet = models.ForeignKey('Tweet',
		on_delete=models.CASCADE,
		related_name='+', blank=True, null=True)
	comment = models.ForeignKey('Comment',
		on_delete=models.CASCADE,
		related_name='comment_notifications',
		blank=True, null=True)
	created_at = models.DateTimeField(default=timezone.now)
	account_has_seen = models.BooleanField(default=False)

	def __str__(self):
		if self.notification_type == 'comment':
			return f'{self.from_user} left the comment to tweet "{self.comment.tweet.text[:20]}..." {self.created_at}'
		elif self.notification_type == 'like':
			return f'{self.from_user} liked the tweet "{self.tweet.text[:50]}..." {self.created_at}'