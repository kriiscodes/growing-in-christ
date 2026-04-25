from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from core.utils import get_active_week, get_previous_week

from .forms import MidweekReflectionForm, SaturdayTakeawayForm
from .models import CheckInAnswer, CheckInQuestion, JourneyCheckIn, MidweekReflection, SaturdayTakeaway


@login_required
def growth_history(request):
    takeaways = (
        SaturdayTakeaway.objects
        .filter(user=request.user)
        .select_related('week')
        .order_by('-week__start_date')
    )
    reflections = (
        MidweekReflection.objects
        .filter(user=request.user)
        .select_related('week')
        .order_by('-week__start_date')
    )

    weeks_map = {}
    for t in takeaways:
        weeks_map.setdefault(t.week.pk, {'week': t.week, 'takeaway': None, 'reflection': None})
        weeks_map[t.week.pk]['takeaway'] = t
    for r in reflections:
        weeks_map.setdefault(r.week.pk, {'week': r.week, 'takeaway': None, 'reflection': None})
        weeks_map[r.week.pk]['reflection'] = r

    history = sorted(weeks_map.values(), key=lambda x: x['week'].start_date, reverse=True)

    return render(request, 'growth/history.html', {'history': history})


@login_required
def checkin(request):
    active_week = get_active_week()
    if not active_week:
        return render(request, 'growth/unavailable.html', {'reason': 'no_week'})

    questions = CheckInQuestion.objects.filter(is_active=True)
    checkin_obj = JourneyCheckIn.objects.filter(user=request.user, week=active_week).first()
    is_edit = checkin_obj is not None

    def build_question_context(post_data=None):
        boolean_ctx = []
        text_ctx = []
        existing_answers = {}
        if checkin_obj:
            for ans in checkin_obj.answers.select_related('question'):
                existing_answers[ans.question_id] = ans

        for q in questions:
            if q.field_type == CheckInQuestion.FieldType.BOOLEAN:
                if post_data is not None:
                    checked = f"question_{q.id}" in post_data
                elif q.id in existing_answers:
                    checked = existing_answers[q.id].boolean_answer
                else:
                    checked = False
                boolean_ctx.append({'q': q, 'checked': checked})
            else:
                if post_data is not None:
                    text_value = post_data.get(f"question_{q.id}", '').strip()
                elif q.id in existing_answers:
                    text_value = existing_answers[q.id].text_answer
                else:
                    text_value = ''
                text_ctx.append({'q': q, 'text_value': text_value})

        return boolean_ctx, text_ctx

    if request.method == 'POST':
        errors = []
        answers = {}
        has_meaningful = False

        for q in questions:
            key = f"question_{q.id}"
            if q.field_type == CheckInQuestion.FieldType.BOOLEAN:
                value = key in request.POST
                answers[q] = value
                if value:
                    has_meaningful = True
            else:
                value = request.POST.get(key, '').strip()
                if q.is_required and not value:
                    errors.append(f'"{q.label}" is required.')
                answers[q] = value
                if value:
                    has_meaningful = True

        required_text_questions = [q for q in questions if q.is_required and q.field_type != CheckInQuestion.FieldType.BOOLEAN]
        if not errors and not required_text_questions and not has_meaningful:
            errors.append('Please share at least one answer before submitting.')

        if not errors:
            if checkin_obj:
                for q, value in answers.items():
                    if q.field_type == CheckInQuestion.FieldType.BOOLEAN:
                        CheckInAnswer.objects.update_or_create(
                            checkin=checkin_obj, question=q,
                            defaults={'boolean_answer': value},
                        )
                    else:
                        CheckInAnswer.objects.update_or_create(
                            checkin=checkin_obj, question=q,
                            defaults={'text_answer': value},
                        )
            else:
                checkin_obj = JourneyCheckIn.objects.create(user=request.user, week=active_week)
                for q, value in answers.items():
                    if q.field_type == CheckInQuestion.FieldType.BOOLEAN:
                        CheckInAnswer.objects.create(checkin=checkin_obj, question=q, boolean_answer=value)
                    else:
                        CheckInAnswer.objects.create(checkin=checkin_obj, question=q, text_answer=value)
            return redirect('core:dashboard')

        boolean_ctx, text_ctx = build_question_context(post_data=request.POST)
        return render(request, 'growth/checkin_form.html', {
            'boolean_question_context': boolean_ctx,
            'text_question_context': text_ctx,
            'errors': errors,
            'is_edit': is_edit,
        })

    boolean_ctx, text_ctx = build_question_context()
    return render(request, 'growth/checkin_form.html', {
        'boolean_question_context': boolean_ctx,
        'text_question_context': text_ctx,
        'is_edit': is_edit,
    })


@login_required
def takeaway(request):
    active_week = get_active_week()
    if not active_week:
        return render(request, 'growth/unavailable.html', {'reason': 'no_week'})

    instance = SaturdayTakeaway.objects.filter(user=request.user, week=active_week).first()
    is_edit = instance is not None

    if request.method == 'POST':
        form = SaturdayTakeawayForm(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.week = active_week
            obj.save()
            return redirect('core:dashboard')
    else:
        form = SaturdayTakeawayForm(instance=instance)

    return render(request, 'growth/takeaway_form.html', {'form': form, 'is_edit': is_edit})


@login_required
def midweek_reflection(request):
    active_week = get_active_week()
    if not active_week:
        return render(request, 'growth/unavailable.html', {'reason': 'no_week'})

    previous_week = get_previous_week(active_week)
    if not previous_week:
        return render(request, 'growth/reflection_unavailable.html', {'reason': 'no_previous_week'})

    previous_takeaway = SaturdayTakeaway.objects.filter(
        user=request.user, week=previous_week
    ).first()
    if not previous_takeaway:
        return render(request, 'growth/reflection_unavailable.html', {
            'reason': 'no_takeaway',
            'previous_week': previous_week,
        })

    instance = MidweekReflection.objects.filter(user=request.user, week=previous_week).first()
    is_edit = instance is not None

    if request.method == 'POST':
        form = MidweekReflectionForm(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.week = previous_week
            obj.save()
            return redirect('core:dashboard')
    else:
        form = MidweekReflectionForm(instance=instance)

    return render(request, 'growth/midweek_reflection_form.html', {
        'form': form,
        'is_edit': is_edit,
        'previous_week': previous_week,
        'previous_takeaway': previous_takeaway,
    })
