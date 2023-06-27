from django.contrib import admin

from .models import Bundle


@admin.register(Bundle)
class BundleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "removed_at", "parent_pack_code")

    def get_queryset(self, request):
        return self.model.all_objects.all()
