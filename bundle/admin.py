from django.contrib import admin

from .models import Bundle


@admin.register(Bundle)
class BundleAdmin(admin.ModelAdmin):
    pass
