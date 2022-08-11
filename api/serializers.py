from rest_framework import serializers

from chat.models import Chat, Message
from tweet.models import Tweet, Comment
from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
	# chat_messages = MessageSerializer(many=True)
	avatar = serializers.StringRelatedField(default=None)
	username = serializers.StringRelatedField(default=None)
	last_message = serializers.StringRelatedField(default=None)
	last_message_date = serializers.DateTimeField(default=None)
	class Meta:
		model = Chat
		fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tweet
		fields = '__all__'


class TweetSerializer(serializers.ModelSerializer):
	comments_count = serializers.IntegerField()
	retweeted_count = serializers.IntegerField()
	liked_count = serializers.IntegerField()
	# account = AccountSerializer()
	# last_liked_by = serializers.IntegerField()
	# last_retweeted_by = serializers.IntegerField()
	class Meta:
		model = Tweet
		fields = '__all__'