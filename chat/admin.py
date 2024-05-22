from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Message , Room 


admin.site.register(Message)
admin.site.register(Room)

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('bio', 'location')}),
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         (None, {'fields': ('bio', 'location')}),
#     )

# admin.site.register(CustomUser, CustomUserAdmin)