from django.contrib import admin

from .models import PrayerEntry


@admin.register(PrayerEntry)
class PrayerEntryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "is_answered", "answered_at", "created_at")
    list_filter = ("is_answered",)
    search_fields = ("title", "user__full_name", "user__email")
    ordering = ("-created_at",)
