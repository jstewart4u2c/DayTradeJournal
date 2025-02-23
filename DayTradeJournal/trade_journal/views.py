from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, login
from .forms import TradeEntryForm
from .models import TradeEntry


# Create your views here.
def home(request):
    user_entries = TradeEntry.objects.filter(user=request.user).order_by('-date', '-time')

    for trade in user_entries:
        if trade.exit_price is not None:
            trade.result = (trade.exit_price - trade.entry_price)*trade.quantity
        else:
            trade.result = None

    return render(request, 'journal/home.html',  {'user_entries': user_entries})


def analysis(request):
    charts = 'Chart analysis coming soon'

    return render(request, 'journal/analysis.html', {'charts': charts})


def calendar(request):
    soon = 'There will be a calendar here'
    return render(request, 'journal/calendar.html', {'soon': soon})


@login_required
def new_entry(request):
    if request.method == 'POST':
        form = TradeEntryForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('journal:home')
    else:
        form = TradeEntryForm()

    return render(request, 'journal/new_entry.html', {'form': form})
