from django.contrib import admin
from .models import Profile, Group, Invite
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'date_joined', 'unique_id']

class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']

class InviteAdmin(admin.ModelAdmin):
    list_display = ['group', 'profile']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Invite, InviteAdmin)