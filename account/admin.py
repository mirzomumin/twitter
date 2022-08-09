from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AccountCreationForm, AccountChangeForm
from .models import Account
# Register your models here.


class AccountAdmin(UserAdmin):
	add_form = AccountCreationForm
	form = AccountChangeForm
	model = Account
	list_display = ('username', 'email', 'phone', 'gender', 'birth_date', 'is_staff')
	fieldsets = UserAdmin.fieldsets + (
		(None, {'fields': ('phone', 'gender', 'birth_date',)}),
	)
	add_fieldsets = UserAdmin.add_fieldsets + (
		(None, {'fields': ('email', 'phone', 'gender', 'birth_date',)}),
	)

admin.site.register(Account, AccountAdmin)