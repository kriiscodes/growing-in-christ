from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.template.loader import render_to_string

from accounts.models import User
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


@login_required
def leader_overview(request):
    if not request.user.is_leader:
        return redirect('core:dashboard')

    active_week = get_active_week()
    previous_week = get_previous_week(active_week) if active_week else None

    members = User.objects.filter(is_active=True).exclude(pk=request.user.pk).order_by('full_name')

    member_data = []
    for member in members:
        checkin = None
        takeaway = None
        reflection = None

        if active_week:
            checkin = JourneyCheckIn.objects.filter(user=member, week=active_week).first()
            takeaway = SaturdayTakeaway.objects.filter(user=member, week=active_week).first()

        if previous_week:
            reflection = MidweekReflection.objects.filter(user=member, week=previous_week).first()

        member_data.append({
            'user': member,
            'checkin': checkin,
            'takeaway': takeaway,
            'reflection': reflection,
        })

    checkin_count  = sum(1 for m in member_data if m['checkin'])
    takeaway_count = sum(1 for m in member_data if m['takeaway'])

    return render(request, 'core/leader_overview.html', {
        'active_week': active_week,
        'previous_week': previous_week,
        'member_data': member_data,
        'member_count': len(member_data),
        'checkin_count': checkin_count,
        'takeaway_count': takeaway_count,
    })


@login_required
def leader_member_detail(request, user_id):
    if not request.user.is_leader:
        return redirect('core:dashboard')

    member = get_object_or_404(User, pk=user_id, is_active=True)
    active_week = get_active_week()
    previous_week = get_previous_week(active_week) if active_week else None

    checkin = None
    checkin_answers = []
    takeaway = None
    reflection = None

    if active_week:
        checkin = JourneyCheckIn.objects.filter(user=member, week=active_week).first()
        if checkin:
            checkin_answers = checkin.answers.select_related('question').order_by('question__sort_order')
        takeaway = SaturdayTakeaway.objects.filter(user=member, week=active_week).first()

    if previous_week:
        reflection = MidweekReflection.objects.filter(user=member, week=previous_week).first()

    return render(request, 'core/leader_member_detail.html', {
        'member': member,
        'active_week': active_week,
        'previous_week': previous_week,
        'checkin': checkin,
        'checkin_answers': checkin_answers,
        'takeaway': takeaway,
        'reflection': reflection,
    })
