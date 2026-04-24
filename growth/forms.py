from django import forms

from .models import MidweekReflection, SaturdayTakeaway

_textarea_classes = (
    'w-full bg-[#FFFCF7] rounded-xl px-4 py-3 text-[#383831] '
    'border border-[#383831]/15 '
    'focus:outline-none focus:shadow-[0_0_0_3px_rgba(105,93,74,0.14)] text-base resize-none'
)

_select_classes = (
    'w-full bg-[#FFFCF7] rounded-xl px-4 py-3 text-[#383831] text-base cursor-pointer '
    'focus:outline-none focus:shadow-[0_0_0_3px_rgba(105,93,74,0.14)]'
)


class SaturdayTakeawayForm(forms.ModelForm):
    class Meta:
        model = SaturdayTakeaway
        fields = ['action_step']
        widgets = {
            'action_step': forms.Textarea(attrs={
                'placeholder': 'One step you will take this week…',
                'rows': 6,
                'class': _textarea_classes,
            }),
        }


class MidweekReflectionForm(forms.ModelForm):
    class Meta:
        model = MidweekReflection
        fields = ['status', 'note']
        widgets = {
            'status': forms.Select(attrs={
                'class': _select_classes,
            }),
            'note': forms.Textarea(attrs={
                'placeholder': 'Any thoughts to share…',
                'rows': 4,
                'class': _textarea_classes,
            }),
        }
