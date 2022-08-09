from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.db import models

from account.models import Account
from tweet.models import Notification, Tweet, Comment


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
	if created:
		notification = Notification.objects.create(notification_type='comment',
		from_user=instance.account, to_user=instance.tweet.account, comment=instance)


@receiver(m2m_changed, sender=Tweet.liked_by.through)
def create_like_notification(sender, instance, action, **kwargs):
	if action == 'post_add':
		account = instance.liked_by.last()
		if account:
			notification = Notification.objects.create(notification_type='like',
				from_user=account, to_user=instance.account, tweet=instance)