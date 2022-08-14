from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from django.db import models

from .permissions import IsMember
from tweet.models import Tweet, Comment
from chat.models import Chat, Message
from account.models import Account
from .serializers import (
	CommentSerializer,
	TweetSerializer,
	ChatSerializer,
	MessageSerializer,
	AccountSerializer,
	ProfileSerializer)
# Create your views here.


class TweetListView(generics.ListAPIView):
	'''Display all tweets'''
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	serializer_class = TweetSerializer

	def get_queryset(self):
		queryset = Tweet.objects.annotate(
			comments_count = models.Count('comments', distinct=True),
			retweeted_count = models.Count('retweeted_by', distinct=True),
			liked_count = models.Count('liked_by', distinct=True),
			# last_liked_by = Tweet.objects.values('liked_by')[1],
			# last_retweeted_by = Tweet.objects.values('retweeted_by')[1]
		)
		return queryset


class TweetDetailView(generics.RetrieveAPIView):
	'''Display detail chat'''
	serializer_class = TweetSerializer

	def get_queryset(self):
		queryset = Tweet.objects.annotate(
			retweeted_count = models.Count('retweeted_by', distinct=True),
			liked_count = models.Count('liked_by', distinct=True),
		)
		return queryset


class TweetCommentsView(generics.ListCreateAPIView):
	'''Comments of the tweet'''
	serializer_class = CommentSerializer

	def get_queryset(self):
		pk = self.kwargs['pk']
		if pk:
			queryset = Comment.objects.filter(tweet__id=pk)
		return queryset

	def perform_create(self, serializer):
		pk = self.kwargs['pk']
		tweet = Tweet.objects.get(id=pk)
		serializer.save(account=self.request.user, tweet=tweet)


class ChatListView(generics.ListAPIView):
	'''All chats of current account'''
	permission_classes = (permissions.IsAuthenticated,)
	search_fields = ['username']
	filter_backends = (filters.SearchFilter,)
	serializer_class = ChatSerializer
	def get_queryset(self):
		queryset = Chat.objects.filter(members=self.request.user).annotate(
			last_message = (Message.objects
				.order_by('-created_at')
				.filter(chat__id=models.OuterRef('id'))
				.values('message')[:1]),
			last_message_date = (Message.objects
				.order_by('-created_at')
				.filter(chat__id=models.OuterRef('id'))
				.values('created_at')[:1]),
			avatar = (Account.objects
				.exclude(id=self.request.user.id)
				.filter(chats__id=models.OuterRef('id'))
				.values('avatar')[:1]
				),
			username = (Account.objects
				.exclude(id=self.request.user.id)
				.filter(chats__id=models.OuterRef('id'))
				.values('username')[:1]
				),
		)
		return queryset


class ChatDetailView(generics.ListCreateAPIView):
	'''Detail chat with all messages'''
	serializer_class = MessageSerializer
	permission_classes = (permissions.IsAuthenticated, IsMember,)
	def get_queryset(self):
		pk = self.kwargs['pk']
		if pk:
			queryset = Message.objects.filter(chat__id=pk)
			print(self.request.user.id)
			return queryset

	def perform_create(self, serializer):
		pk = self.kwargs['pk']
		chat = Chat.objects.get(id=pk)
		serializer.save(user=self.request.user, chat=chat)


class MembersListView(generics.ListCreateAPIView):
	'''Display followers and followings list'''
	serializer_class = AccountSerializer
	def get_queryset(self):
		queryset = Account.objects.filter(id=self.request.user.id)
		return queryset


class AccountProfileView(generics.RetrieveUpdateAPIView):
	'''Profile of current user'''
	serializer_class = ProfileSerializer
	permission_classes = (permissions.IsAuthenticated,)
	def get_queryset(self):
		queryset = Account.objects.filter(id=self.request.user.id).annotate(
			followings_count = models.Count('followings', distinct=True),
			followers_count = models.Count('followers', distinct=True),
		)
		return queryset