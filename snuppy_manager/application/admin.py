from django.contrib import admin

from .models import Application, Version

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'description', 'created_at', 'updated_at']

class VersionAdmin(admin.ModelAdmin):
    list_display = ['number', 'application', 'path', 'created_at', 'updated_at']

# Register your models here.
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Version, VersionAdmin)
