from django.contrib import admin
from .models import Profile, Application, Version
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'date_joined', 'unique_id']

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'description', 'created_at', 'updated_at']

class VersionAdmin(admin.ModelAdmin):
    list_display = ['number', 'application', 'path', 'created_at', 'updated_at']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Version, VersionAdmin)