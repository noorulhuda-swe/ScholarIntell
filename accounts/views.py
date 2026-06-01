from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm, StudentProfileForm
from .models import StudentProfile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created! Please complete your profile.')
            return redirect('profile_setup')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def profile_setup(request):
    profile, created = StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={'cgpa': 0.0, 'degree_level': 'Bachelor', 'field_of_study': '', 'country_of_origin': ''}
    )
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=profile)
        if form.is_valid():
            p = form.save(commit=False)
            p.profile_complete = True
            p.save()
            messages.success(request, 'Profile saved! Here are your scholarship recommendations.')
            return redirect('dashboard')
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, 'accounts/profile_setup.html', {'form': form})
