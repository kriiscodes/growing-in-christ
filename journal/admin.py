from django.contrib import admin

from .models import JournalEntry


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "entry_type", "created_at")
    list_filter = ("entry_type",)
    search_fields = ("user__full_name", "user__email")
    ordering = ("-created_at",)
