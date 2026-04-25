from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import JournalEntryForm
from .models import JournalEntry


@login_required
def journal_home(request):
    entries = JournalEntry.objects.filter(user=request.user)
    return render(request, 'journal/journal_home.html', {'journal_entries': entries})


@login_required
def journal_detail(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, user=request.user)
    return render(request, 'journal/journal_detail.html', {'entry': entry})


@login_required
def new_entry(request):
    form = JournalEntryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        entry = form.save(commit=False)
        entry.user = request.user
        entry.save()
        return redirect('journal:journal_home')
    return render(request, 'journal/journal_form.html', {'form': form})


@login_required
def edit_entry(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, user=request.user)
    form = JournalEntryForm(request.POST or None, instance=entry)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('journal:journal_detail', pk=entry.pk)
    return render(request, 'journal/journal_form.html', {'form': form, 'is_edit': True, 'entry': entry})


@login_required
def delete_entry(request, pk):
    if request.method == 'POST':
        entry = get_object_or_404(JournalEntry, pk=pk, user=request.user)
        entry.delete()
    return redirect('journal:journal_home')
