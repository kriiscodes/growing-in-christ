from django import forms

from .models import JournalEntry

_field_classes = (
    'w-full bg-[#FFFCF7] rounded-xl px-4 py-3 text-[#383831] placeholder-[#BABAB0] '
    'focus:outline-none focus:shadow-[0_0_0_3px_rgba(105,93,74,0.14)] text-base'
)


class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['entry_type', 'content']
        widgets = {
            'entry_type': forms.Select(attrs={
                'class': _field_classes + ' cursor-pointer',
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write here…',
                'rows': 7,
                'class': _field_classes + ' resize-none',
            }),
        }
