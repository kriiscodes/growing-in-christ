from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.utils import get_active_week


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
