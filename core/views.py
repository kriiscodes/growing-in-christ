from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.template.loader import render_to_string

from announcements.models import Announcement
from growth.models import JourneyCheckIn, MidweekReflection, SaturdayTakeaway
from .utils import get_active_week, get_previous_week


@login_required
def dashboard(request):
    active_week = get_active_week()

    weekly_word = None
    prayer_focus = None
    meeting_info = None

    if active_week:
        weekly_word = getattr(active_week, 'weekly_word', None)
        if weekly_word and not weekly_word.is_published:
            weekly_word = None

        prayer_focus = getattr(active_week, 'prayer_focus', None)
        meeting_info = getattr(active_week, 'meeting_info', None)

    latest_announcement = (
        Announcement.objects.filter(is_published=True).order_by('-created_at').first()
    )

    checkin_done = False
    takeaway_done = False
    reflection_done = False
    reflection_available = False

    if active_week:
        checkin_done = JourneyCheckIn.objects.filter(user=request.user, week=active_week).exists()
        takeaway_done = SaturdayTakeaway.objects.filter(user=request.user, week=active_week).exists()

        previous_week = get_previous_week(active_week)
        if previous_week:
            has_previous_takeaway = SaturdayTakeaway.objects.filter(
                user=request.user, week=previous_week
            ).exists()
            if has_previous_takeaway:
                reflection_available = True
                reflection_done = MidweekReflection.objects.filter(
                    user=request.user, week=previous_week
                ).exists()

    context = {
        "active_week": active_week,
        "weekly_word": weekly_word,
        "prayer_focus": prayer_focus,
        "meeting_info": meeting_info,
        "latest_announcement": latest_announcement,
        "checkin_done": checkin_done,
        "takeaway_done": takeaway_done,
        "reflection_done": reflection_done,
        "reflection_available": reflection_available,
    }
    return render(request, 'core/dashboard.html', context)


@never_cache
def service_worker(request):
    content = render_to_string('pwa/service-worker.js', request=request)
    return HttpResponse(content, content_type='application/javascript')


@never_cache
def manifest(request):
    content = render_to_string('pwa/manifest.webmanifest', request=request)
    return HttpResponse(content, content_type='application/manifest+json')


def offline(request):
    return render(request, 'pwa/offline.html')


def create_admin(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if User.objects.filter(is_superuser=True).exists():
        return HttpResponse('Admin already exists.')
    User.objects.create_superuser(email='emenikechristopher0@gmail.com', full_name='Admin User', password='admin1234')
    return HttpResponse('Superuser created: emenikechristopher0@gmail.com / admin1234')
