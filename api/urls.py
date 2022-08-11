from django.urls import path

from . import views


urlpatterns = [
	path('tweets/', views.TweetListView.as_view()),
	path('tweets/<int:pk>/comments/', views.TweetCommentsView.as_view()),
	path('chats/', views.ChatListView.as_view()),
	path('chats/<int:pk>/', views.ChatDetailView.as_view()),
]