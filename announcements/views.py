from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Announcement


@login_required
def announcement_list(request):
    announcements = Announcement.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'announcements/announcement_list.html', {
        'announcements': announcements,
    })
