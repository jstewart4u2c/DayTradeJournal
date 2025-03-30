from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, login
from .forms import TradeEntryForm
from .models import TradeEntry


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        user_entries = TradeEntry.objects.filter(user=request.user).order_by('-date')

        frameworks = TradeEntry._meta.get_field('framework').choices
        strategies = TradeEntry._meta.get_field('strategy').choices

        framework_filter = request.GET.get('framework')
        if framework_filter:
            user_entries = user_entries.filter(framework=framework_filter)

        strategies_filter = request.GET.get('strategy')
        if strategies_filter:
            user_entries = user_entries.filter(strategy=strategies_filter)

        result_filter = request.GET.get('result')
        if result_filter == 'positive':
            user_entries = [trade for trade in user_entries if trade.calculate_result() > 0]
        elif result_filter == 'negative':
            user_entries = [trade for trade in user_entries if trade.calculate_result() < 0]

    else:
        user_entries = []

    return render(request, 'journal/home.html',  {
        'user_entries': user_entries,
        'frameworks': frameworks,
        'strategies': strategies,
    })


def analysis(request):
    charts = 'Chart analysis coming soon'
    return render(request, 'journal/analysis.html', {'charts': charts})


def calendar(request):
    if request.user.is_authenticated:
        user_entries = TradeEntry.objects.filter(user=request.user).order_by('-date')

        # Calculate total money won/lost per day
        daily_results = defaultdict(float)

        for trade in user_entries:
            result = trade.calculate_result()
            if result is not None:
                daily_results[trade.date] += float(result)

        # Convert daily results to calendar events
        trade_events = [
            {
                'title': f"${total_result:.2f}",
                'start': trade_date.isoformat(),
                'color': 'green' if total_result > 0 else 'red',
            }
            for trade_date, total_result in daily_results.items()
        ]

        print(trade_events)  # Debugging step

    else:
        trade_events = []

    return render(request, 'journal/calendar.html', {
        'trade_events': trade_events
    })


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


def edit_entry(request, pk):
    entry = TradeEntry.objects.filter(id=pk).first()

    if not entry:
        return redirect('journal:home')

    if request.method == 'POST':
        form = TradeEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('journal:home')

    else:
        form = TradeEntryForm(instance=entry)

    return render(request, 'journal/edit_entry.html', {'form': form, 'entry': entry})


def delete_entry(request, pk):
    entry = TradeEntry.objects.filter(id=pk)

    if entry:
        entry.delete()
        messages.success(request, "Trade entry deleted successfully.")

    return redirect('journal:home')