from django.contrib import admin

from .models import Application

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'description', 'created_at', 'updated_at']


# Register your models here.
admin.site.register(Application, ApplicationAdmin)
