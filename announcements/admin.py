from django.contrib import admin

from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "is_published", "created_at")
    list_filter = ("is_published",)
    search_fields = ("title", "created_by__full_name")
    ordering = ("-created_at",)
