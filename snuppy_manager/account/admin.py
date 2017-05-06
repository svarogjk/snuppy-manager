from django.contrib import admin
from .models import Profile, Application, Version, Group, Invite
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'date_joined', 'unique_id']

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'description', 'created_at', 'updated_at']

class VersionAdmin(admin.ModelAdmin):
    list_display = ['number', 'application', 'path', 'created_at', 'updated_at']

class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']

class InviteAdmin(admin.ModelAdmin):
    list_display = ['group', 'profile']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Invite, InviteAdmin)