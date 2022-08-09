from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Account(AbstractUser):
	"""Custom user account of Twitter app"""

	GENDER = (
		('male', 'Male'),
		('female', 'Female')
	)
	first_name = models.CharField(max_length=50, blank=False, null=True)
	last_name = models.CharField(max_length=50, blank=False, null=True)
	avatar = models.ImageField(upload_to='media/avatar/', null=True, blank=True, default='')
	email = models.EmailField(unique=True, null=False, blank=False)
	phone = PhoneNumberField(unique=True, null=True)
	gender = models.CharField(max_length=10, choices=GENDER, null=True)
	birth_date = models.DateField(null=True)

	bio = models.TextField()
	url = models.URLField(blank=True, null=True)
	is_verified = models.BooleanField(default=False)
	is_online = models.BooleanField(default=False)

	followings = models.ManyToManyField('self')
	followers = models.ManyToManyField('self')

	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)

	def follow(self, another_account):
		"""Follow to another account"""
		self.followings.add(another_account)
		another_account.followers.add(self)

	def unfollow(self, another_account):
		"""Unfollow to another account"""
		self.followings.remove(another_account)
		another_account.followers.remove(self)

	def __str__(self):
		"""Simple representation of model"""
		return self.username