from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from core.utils import get_active_week
from weeks.models import Week


@login_required
def weekly_word(request):
    active_week = get_active_week()

    word = None
    resources = []

    if active_week:
        candidate = getattr(active_week, 'weekly_word', None)
        if candidate and candidate.is_published:
            word = candidate
            resources = list(word.resources.all())

    context = {
        'active_week': active_week,
        'weekly_word': word,
        'resources': resources,
    }
    return render(request, 'studies/weekly_word.html', context)


@login_required
def archive(request):
    past_weeks = (
        Week.objects
        .filter(weekly_word__is_published=True, is_active=False)
        .select_related('weekly_word')
        .order_by('-start_date')
    )
    return render(request, 'studies/archive.html', {'past_weeks': past_weeks})


@login_required
def archive_week(request, pk):
    week = get_object_or_404(Week, pk=pk, is_active=False, weekly_word__is_published=True)
    word = week.weekly_word
    resources = list(word.resources.all())
    return render(request, 'studies/archive_week.html', {
        'week': week,
        'weekly_word': word,
        'resources': resources,
    })
