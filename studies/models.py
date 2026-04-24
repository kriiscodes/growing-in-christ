from django.core.exceptions import ValidationError
from django.db import models

from core.models import TimeStampedModel


class WeeklyWord(TimeStampedModel):
    week = models.OneToOneField("weeks.Week", on_delete=models.CASCADE, related_name="weekly_word")
    scripture_references = models.CharField(max_length=500, blank=True)
    content = models.TextField()
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.PROTECT, related_name="weekly_words"
    )
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ["-week__start_date"]

    def __str__(self):
        return self.scripture_references or str(self.week)

    def clean(self):
        if self.created_by_id and not self.created_by.is_leader:
            raise ValidationError("created_by must be a leader.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class StudyResource(TimeStampedModel):
    weekly_word = models.ForeignKey(
        WeeklyWord, on_delete=models.CASCADE, related_name="resources"
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="study_resources/", null=True, blank=True)
    external_link = models.URLField(blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def clean(self):
        if not self.file and not self.external_link:
            raise ValidationError("At least one of file or external_link must be provided.")
