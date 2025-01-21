from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout


# Create your views here.
def home(request):
    hello = 'Hello World!'

    return render(request, 'journal/home.html',  {'hello': hello})


def analysis(request):
    charts = 'Chart analysis coming soon'

    return render(request, 'journal/analysis.html', {'charts': charts})


def calendar(request):
    soon = 'There will be a calendar here'
    return render(request, 'journal/calendar.html', {'soon': soon})


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('journal:home')
