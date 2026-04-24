from django.db import models

from core.models import TimeStampedModel



class CheckInQuestion(TimeStampedModel):
    class FieldType(models.TextChoices):
        BOOLEAN = "boolean", "Yes / No toggle"
        SHORT_TEXT = "short_text", "Short text"
        LONG_TEXT = "long_text", "Long text"

    label = models.CharField(max_length=255)
    help_text = models.CharField(max_length=255, blank=True)
    field_type = models.CharField(max_length=20, choices=FieldType.choices, default=FieldType.BOOLEAN)
    is_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "created_at"]

    def __str__(self):
        return self.label


class JourneyCheckIn(TimeStampedModel):
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="journey_checkins"
    )
    week = models.ForeignKey("weeks.Week", on_delete=models.CASCADE, related_name="journey_checkins")

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "week"], name="unique_journey_checkin_per_user_week")
        ]

    def __str__(self):
        return f"{self.user} - {self.week}"


class CheckInAnswer(TimeStampedModel):
    checkin = models.ForeignKey(JourneyCheckIn, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(CheckInQuestion, on_delete=models.CASCADE, related_name="answers")
    boolean_answer = models.BooleanField(null=True, blank=True)
    text_answer = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["checkin", "question"], name="unique_answer_per_checkin_question")
        ]

    def __str__(self):
        return f"{self.checkin} — {self.question}"


class SaturdayTakeaway(TimeStampedModel):
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="saturday_takeaways"
    )
    week = models.ForeignKey("weeks.Week", on_delete=models.CASCADE, related_name="saturday_takeaways")
    action_step = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "week"], name="unique_saturday_takeaway_per_user_week")
        ]

    def __str__(self):
        return f"{self.user} - {self.week}"


class MidweekReflection(TimeStampedModel):
    class Status(models.TextChoices):
        GOING_WELL = "going_well", "Going well"
        STRUGGLING = "struggling", "Struggling"
        NOT_STARTED = "not_started", "Not started"

    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="midweek_reflections"
    )
    week = models.ForeignKey(
        "weeks.Week", on_delete=models.CASCADE, related_name="midweek_reflections"
    )
    status = models.CharField(max_length=20, choices=Status.choices)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "week"], name="unique_midweek_reflection_per_user_week")
        ]

    def __str__(self):
        return f"{self.user} - {self.week}"
