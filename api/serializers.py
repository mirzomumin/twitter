from rest_framework import serializers

from tweet.models import Tweet, Comment
from account.models import Account


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