from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.utils import get_active_week
from .forms import PrayerEntryForm
from .models import PrayerEntry


@login_required
def prayer_home(request):
    active_week = get_active_week()
    prayer_focus = None
    if active_week:
        prayer_focus = getattr(active_week, 'prayer_focus', None)

    prayer_entries = PrayerEntry.objects.filter(user=request.user)
    answered_count = prayer_entries.filter(is_answered=True).count()

    context = {
        'active_week': active_week,
        'prayer_focus': prayer_focus,
        'prayer_entries': prayer_entries,
        'answered_count': answered_count,
    }
    return render(request, 'prayer/prayer_home.html', context)


@login_required
def prayer_detail(request, pk):
    entry = get_object_or_404(PrayerEntry, pk=pk, user=request.user)
    return render(request, 'prayer/prayer_detail.html', {'entry': entry})


@login_required
def new_prayer(request):
    form = PrayerEntryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        entry = form.save(commit=False)
        entry.user = request.user
        entry.save()
        return redirect('prayer:prayer_home')

    return render(request, 'prayer/prayer_form.html', {'form': form})


@login_required
def edit_prayer(request, pk):
    entry = get_object_or_404(PrayerEntry, pk=pk, user=request.user)
    form = PrayerEntryForm(request.POST or None, instance=entry)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('prayer:prayer_detail', pk=entry.pk)
    return render(request, 'prayer/prayer_form.html', {'form': form, 'is_edit': True, 'entry': entry})


@login_required
def delete_prayer(request, pk):
    if request.method == 'POST':
        entry = get_object_or_404(PrayerEntry, pk=pk, user=request.user)
        entry.delete()
    return redirect('prayer:prayer_home')


@login_required
def mark_answered(request, pk):
    if request.method != 'POST':
        return redirect('prayer:prayer_home')

    entry = get_object_or_404(PrayerEntry, pk=pk, user=request.user)

    if not entry.is_answered:
        entry.is_answered = True
        entry.save()

    return redirect('prayer:prayer_detail', pk=entry.pk)
