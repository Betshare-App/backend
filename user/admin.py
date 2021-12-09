from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAddress, UserBalance, UserContact, UserFinanceInfo, UserDocs
from django.contrib.auth.models import User
# Register your models here.

class AddressInLine(admin.TabularInline):
    model = UserAddress
class BalanceInLine(admin.TabularInline):
    model = UserBalance
class ContactInLine(admin.TabularInline):
    model = UserContact
class FinanceInfoInLine(admin.TabularInline):
    model = UserFinanceInfo
class DocsInLine(admin.TabularInline):
    model = UserDocs


class UserAdmin(UserAdmin):
    list_display = ('username', 
                    'email', 
                    'first_name', 
                    'last_name', 
                    'is_staff')
    inlines = [
                AddressInLine,
                BalanceInLine,
                ContactInLine,
                FinanceInfoInLine,
                DocsInLine
            ]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


    