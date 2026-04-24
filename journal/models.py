from django.db import models

from core.models import TimeStampedModel


class JournalEntry(TimeStampedModel):
    class EntryType(models.TextChoices):
        REFLECTION = "reflection", "Reflection"
        LESSON = "lesson", "Lesson"
        SCRIPTURE = "scripture", "Scripture"
        PRAYER = "prayer", "Prayer"

    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="journal_entries"
    )
    entry_type = models.CharField(max_length=20, choices=EntryType.choices)
    content = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_entry_type_display()} — {self.user} ({self.created_at:%Y-%m-%d})"
