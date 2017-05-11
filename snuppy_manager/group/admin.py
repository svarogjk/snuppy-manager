from django.contrib import admin
from .models import Group, Invite
# Register your models here.

class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']

class InviteAdmin(admin.ModelAdmin):
    list_display = ['group', 'profile']

admin.site.register(Group, GroupAdmin)
admin.site.register(Invite, InviteAdmin)