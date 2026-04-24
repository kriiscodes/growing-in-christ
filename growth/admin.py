from django.contrib import admin

from .models import CheckInAnswer, CheckInQuestion, JourneyCheckIn, MidweekReflection, SaturdayTakeaway


@admin.register(CheckInQuestion)
class CheckInQuestionAdmin(admin.ModelAdmin):
    list_display = ("label", "field_type", "is_required", "is_active", "sort_order")
    list_filter = ("field_type", "is_active", "is_required")
    list_editable = ("sort_order", "is_active")
    ordering = ("sort_order",)


@admin.register(JourneyCheckIn)
class JourneyCheckInAdmin(admin.ModelAdmin):
    list_display = ("user", "week", "created_at")
    list_filter = ("week",)
    search_fields = ("user__full_name", "user__email")
    ordering = ("-week__start_date",)


@admin.register(CheckInAnswer)
class CheckInAnswerAdmin(admin.ModelAdmin):
    list_display = ("checkin", "question", "boolean_answer", "text_answer")
    list_filter = ("question",)
    search_fields = ("checkin__user__full_name", "checkin__user__email")


@admin.register(SaturdayTakeaway)
class SaturdayTakeawayAdmin(admin.ModelAdmin):
    list_display = ("user", "week", "created_at")
    list_filter = ("week",)
    search_fields = ("user__full_name", "user__email")
    ordering = ("-week__start_date",)


@admin.register(MidweekReflection)
class MidweekReflectionAdmin(admin.ModelAdmin):
    list_display = ("user", "week", "status")
    list_filter = ("week", "status")
    search_fields = ("user__full_name", "user__email")
    ordering = ("-week__start_date",)
