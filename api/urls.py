from django.urls import path

from . import views


urlpatterns = [
	path('tweets/', views.TweetListView.as_view()),
	path('tweets/<int:pk>/comments/', views.TweetCommentsView.as_view()),
]