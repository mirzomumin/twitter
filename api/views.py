from rest_framework import generics, permissions
from django.db import models

from tweet.models import Tweet, Comment
from .serializers import CommentSerializer, TweetSerializer
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