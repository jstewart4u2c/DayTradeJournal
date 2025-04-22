from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import RegisterForm, UpdateProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('journal:home')
        else:
            messages.error(request, 'Invalid username or password. Try again.')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('journal:home')


@login_required()
def profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})



