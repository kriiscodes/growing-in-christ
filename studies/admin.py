from django.contrib import admin

from .models import StudyResource, WeeklyWord


class StudyResourceInline(admin.TabularInline):
    model = StudyResource
    extra = 0


@admin.register(WeeklyWord)
class WeeklyWordAdmin(admin.ModelAdmin):
    list_display = ("scripture_references", "week", "created_by", "is_published")
    list_filter = ("is_published",)
    search_fields = ("scripture_references",)
    ordering = ("-week__start_date",)
    inlines = [StudyResourceInline]


@admin.register(StudyResource)
class StudyResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "weekly_word")
    ordering = ("title",)
