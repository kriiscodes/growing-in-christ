from django import forms

from .models import PrayerEntry

_field_classes = (
    'w-full bg-[#FFFCF7] rounded-xl px-4 py-3 text-[#383831] placeholder-[#BABAB0] '
    'focus:outline-none focus:shadow-[0_0_0_3px_rgba(105,93,74,0.14)] text-base'
)


class PrayerEntryForm(forms.ModelForm):
    # Override to make title optional — model omits blank=True but save() skips full_clean()
    title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Title (optional)',
            'class': _field_classes,
        }),
    )

    class Meta:
        model = PrayerEntry
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write here…',
                'rows': 6,
                'class': _field_classes + ' resize-none',
            }),
        }
