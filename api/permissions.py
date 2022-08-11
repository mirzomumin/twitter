from rest_framework import permissions
from django.shortcuts import get_object_or_404
from chat.models import Chat


class IsMember(permissions.BasePermission):
	# def get_object(self):
	# 	obj = get_object_or_404(Chat, pk=self.kwargs["pk"])
	# 	# self.check_object_permissions(self.request, obj)
	# 	return obj
	

	def has_permission(self, request, view):
		return request.user in obj.members.all()