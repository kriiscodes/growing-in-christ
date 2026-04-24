from django.core.exceptions import ValidationError
from django.db import models

from core.models import TimeStampedModel


class Week(TimeStampedModel):
    title = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.title or self.date_label

    @property
    def date_label(self):
        start = f"{self.start_date.strftime('%B')} {self.start_date.day}"
        end = f"{self.end_date.strftime('%B')} {self.end_date.day}"
        return f"{start} – {end}"

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("start_date must be on or before end_date.")

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.is_active:
            Week.objects.exclude(pk=self.pk).filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)


class MeetingInfo(TimeStampedModel):
    week = models.OneToOneField(Week, on_delete=models.CASCADE, related_name="meeting_info")
    meeting_time = models.DateTimeField()
    meeting_note = models.TextField(blank=True)

    class Meta:
        ordering = ["-week__start_date"]

    def __str__(self):
        return f"Meeting info for {self.week}"


class PrayerFocus(TimeStampedModel):
    week = models.OneToOneField(Week, on_delete=models.CASCADE, related_name="prayer_focus")
    content = models.TextField()

    class Meta:
        ordering = ["-week__start_date"]

    def __str__(self):
        return f"Prayer focus for {self.week}"
