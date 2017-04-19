from django.contrib import admin
from .models import Profile, Application, Version
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'unique_id']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Application)
admin.site.register(Version)