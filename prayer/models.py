from django.utils import timezone
from django.db import models

from core.models import TimeStampedModel


class PrayerEntry(TimeStampedModel):
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="prayer_entries"
    )
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    is_answered = models.BooleanField(default=False)
    answered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_answered and not self.answered_at:
            self.answered_at = timezone.now()
        elif not self.is_answered:
            self.answered_at = None
        super().save(*args, **kwargs)
