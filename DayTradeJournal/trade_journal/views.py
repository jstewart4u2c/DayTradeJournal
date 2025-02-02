from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, login
from .forms import TradeEntryForm


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


def new_entry(request):
    if request.method == 'POST':
        form = TradeEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('journal:home')
    else:
        form = TradeEntryForm()

    return render(request, 'journal/new_entry.html', {'form': form})



