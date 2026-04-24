from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LoginForm, SignupForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        next_url = request.GET.get('next')
        if next_url and next_url.startswith('/'):
            return redirect(next_url)
        return redirect('core:dashboard')

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('core:dashboard')

    return render(request, 'accounts/signup.html', {'form': form})
