from django.core.exceptions import ValidationError
from django.db import models

from core.models import TimeStampedModel


class Announcement(TimeStampedModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.PROTECT, related_name="announcements"
    )
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def clean(self):
        if self.created_by_id and not self.created_by.is_leader:
            raise ValidationError("created_by must be a leader.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
