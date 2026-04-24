from weeks.models import Week


def get_active_week():
    return Week.objects.filter(is_active=True).first()


def get_previous_week(current_week):
    return (
        Week.objects
        .filter(start_date__lt=current_week.start_date)
        .order_by('-start_date')
        .first()
    )
