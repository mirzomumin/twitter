from rest_framework import generics, permissions
from django.db import models

from .permissions import IsMember
from tweet.models import Tweet, Comment
from chat.models import Chat, Message
from account.models import Account
from .serializers import CommentSerializer, TweetSerializer, ChatSerializer, MessageSerializer
# Create your views here.


class TweetListView(generics.ListAPIView):
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



class TweetCommentsView(generics.ListAPIView):
	serializer_class = CommentSerializer

	def get_queryset(self):
		pk = self.kwargs['pk']
		if pk:
			queryset = Comment.objects.filter(tweet__id=pk)
		return queryset


class ChatListView(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated,)
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
	permission_classes = (permissions.IsAuthenticated, IsMember,)
	serializer_class = MessageSerializer
	def get_queryset(self):
		pk = self.kwargs['pk']
		if pk:
			queryset = Message.objects.filter(chat__id=pk)
		return queryset


# class ChatDetailView(generics.RetrieveDestroyAPIView):
# 	permission_classes = (permissions.IsAuthenticated, IsMember,)
# 	serializer_class = ChatSerializer
# 	queryset = Chat.objects.all()