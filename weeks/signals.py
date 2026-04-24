from datetime import datetime, timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


@receiver(post_save, sender='weeks.Week')
def create_default_meeting_info(sender, instance, created, **kwargs):
    if not created:
        return

    from .models import MeetingInfo

    # start_date is always Sunday; Saturday = start_date + 6 days
    saturday = instance.start_date + timedelta(days=6)
    naive_dt = datetime(saturday.year, saturday.month, saturday.day, 19, 30)
    meeting_time = timezone.make_aware(naive_dt)

    MeetingInfo.objects.get_or_create(
        week=instance,
        defaults={'meeting_time': meeting_time},
    )
