from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Message, Room

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'location')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'location')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Message)
admin.site.register(Room)
