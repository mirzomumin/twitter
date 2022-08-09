from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Account


class AccountCreationForm(UserCreationForm):
	class Meta:
		model = Account
		fields = ['first_name', 'last_name', 'email', 'phone', 'gender', 'birth_date']


class AccountChangeForm(UserChangeForm):
	class Meta:
		model = Account
		fields = UserChangeForm.Meta.fields