from django.contrib import admin
from .models import Version
# Register your models here.


class VersionAdmin(admin.ModelAdmin):
    list_display = ['number', 'application', 'path', 'created_at', 'updated_at']

# Register your models here.
admin.site.register(Version, VersionAdmin)
