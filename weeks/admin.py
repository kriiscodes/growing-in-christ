from django.contrib import admin

from .models import MeetingInfo, PrayerFocus, Week


class MeetingInfoInline(admin.StackedInline):
    model = MeetingInfo
    extra = 0


class PrayerFocusInline(admin.StackedInline):
    model = PrayerFocus
    extra = 0


@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    list_display = ("start_date", "end_date", "title", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title",)
    ordering = ("-start_date",)
    inlines = [MeetingInfoInline, PrayerFocusInline]


@admin.register(MeetingInfo)
class MeetingInfoAdmin(admin.ModelAdmin):
    list_display = ("week", "meeting_time")
    ordering = ("-week__start_date",)


@admin.register(PrayerFocus)
class PrayerFocusAdmin(admin.ModelAdmin):
    list_display = ("week",)
    ordering = ("-week__start_date",)
