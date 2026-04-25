from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

from .models import User

_input_classes = (
    'w-full bg-[#FCF9F3] rounded-xl px-4 py-3.5 text-[#383831] '
    'placeholder-[#BABAB0] border border-[#383831]/15 '
    'focus:outline-none focus:shadow-[0_0_0_3px_rgba(105,93,74,0.14)] text-base'
)


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address',
            'autocomplete': 'email',
            'class': _input_classes,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'autocomplete': 'current-password',
            'class': _input_classes,
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = None

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            self._user = authenticate(username=email, password=password)
            if not self._user:
                raise forms.ValidationError("No account found with those credentials.")
        return cleaned_data

    def get_user(self):
        return self._user


class SignupForm(forms.Form):
    full_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Full name',
            'autocomplete': 'name',
            'class': _input_classes,
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address',
            'autocomplete': 'email',
            'class': _input_classes,
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'autocomplete': 'new-password',
            'class': _input_classes,
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm password',
            'autocomplete': 'new-password',
            'class': _input_classes,
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', "Passwords do not match.")
        return cleaned_data

    def save(self):
        return User.objects.create_user(
            email=self.cleaned_data['email'],
            full_name=self.cleaned_data['full_name'],
            password=self.cleaned_data['password1'],
        )


class StyledPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email address',
            'autocomplete': 'email',
            'class': _input_classes,
        })


class StyledSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'placeholder': 'New password',
            'autocomplete': 'new-password',
            'class': _input_classes,
        })
        self.fields['new_password2'].widget.attrs.update({
            'placeholder': 'Confirm new password',
            'autocomplete': 'new-password',
            'class': _input_classes,
        })
