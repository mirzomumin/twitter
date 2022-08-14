from rest_framework import permissions

from chat.models import Chat


class IsMember(permissions.BasePermission):
	def has_permission(self, request, view):
		pk = view.kwargs.get('pk')
		chat = Chat.objects.get(id=pk)
		return request.user in chat.members.all()