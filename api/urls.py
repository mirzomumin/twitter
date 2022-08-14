from django.urls import path

from . import views


urlpatterns = [
	# All tweets
	path('tweets/', views.TweetListView.as_view()),

	# Detailed tweet
	path('tweets/<int:pk>/', views.TweetDetailView.as_view()),

	# Current tweet comments
	path('tweets/<int:pk>/comments/', views.TweetCommentsView.as_view()),

	# All chats belonged to current user
	path('chats/', views.ChatListView.as_view()),

	# Detailed chat with messages
	path('chats/<int:pk>/', views.ChatDetailView.as_view()),

	# Followers and  Followings list
	path('account/lists/', views.MembersListView.as_view()),

	# Account Profile
	path('account/<int:pk>/profile/', views.AccountProfileView.as_view()),
]