from rest_framework import serializers

from chat.models import Chat, Message
from tweet.models import Tweet, Comment
from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
	'''Account Serializer'''
	class Meta:
		model = Account
		fields = ['followers', 'followings']


class MessageSerializer(serializers.ModelSerializer):
	'''Message Serializer'''
	class Meta:
		model = Message
		fields = '__all__'
		read_only_fields = ['user', 'chat']


class ChatSerializer(serializers.ModelSerializer):
	'''Chat Serializer'''
	avatar = serializers.StringRelatedField(default=None)
	username = serializers.StringRelatedField(default=None)
	last_message = serializers.StringRelatedField(default=None)
	last_message_date = serializers.DateTimeField(default=None)
	class Meta:
		model = Chat
		fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
	'''Comment Serializer'''
	class Meta:
		model = Comment
		fields = '__all__'
		read_only_fields = ['tweet', 'parent', 'liked_by', 'retweeted_by', 'account']


class TweetSerializer(serializers.ModelSerializer):
	'''Tweet Serializer'''
	comments_count = serializers.IntegerField(default=None)
	retweeted_count = serializers.IntegerField(default=None)
	liked_count = serializers.IntegerField(default=None)
	class Meta:
		model = Tweet
		fields = '__all__'


class ProfileTweetSerializer(serializers.ModelSerializer):
	'''Tweet Serializer of User Profile'''
	comments_count = serializers.IntegerField(default=None)
	retweeted_count = serializers.IntegerField(default=None)
	liked_count = serializers.IntegerField(default=None)
	comments = CommentSerializer(many=True)
	class Meta:
		model = Tweet
		fields = (
			'account', 'text', 'media', 'created_at',
			'comments_count', 'retweeted_count',
			'liked_count', 'comments', 'liked_by')


class ProfileSerializer(serializers.ModelSerializer):
	'''Profile Serializer of Account'''
	followings_count = serializers.IntegerField(read_only=True)
	followers_count = serializers.IntegerField(read_only=True)
	tweets = ProfileTweetSerializer(many=True)
	class Meta:
		model = Account
		fields = (
			'username', 'first_name',
			'last_name', 'followings_count',
			'followers_count', 'tweets', 'avatar',
			'email', 'phone', 'gender', 'birth_date',
			'bio', 'url', 'is_online', 'created_at')