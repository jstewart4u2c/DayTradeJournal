from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.forms import FloatField
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, login
from .forms import TradeEntryForm
from .models import TradeEntry
from django.db.models import Q, Count, Sum, F, ExpressionWrapper, DecimalField
from django.core.paginator import Paginator


# Create your views here.
def home(request):
    frameworks = TradeEntry._meta.get_field('framework').choices
    strategies = TradeEntry._meta.get_field('strategy').choices
    user_entries = []
    obj = None

    if request.user.is_authenticated:
        user_entries = TradeEntry.objects.filter(user=request.user).order_by('-date')

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

        paginator = Paginator(user_entries, 10)
        page = request.GET.get('page')
        obj = paginator.get_page(page)

    else:
        user_entries = []

    return render(request, 'journal/home.html',  {
        'user_entries': obj,
        'frameworks': frameworks,
        'strategies': strategies,
        'obj': obj,
    })


def analysis(request):
    if request.user.is_authenticated:
        user = request.user

        trades = TradeEntry.objects.filter(user=user).values('date').annotate(
            profit=Sum('result')
        ).order_by('date')

        profit = []
        total_profit = 0
        dates = []

        for trade in trades:
            total_profit += trade['profit']
            profit.append(total_profit)
            dates.append(trade['date'].strftime('%Y-%m-%d'))

        # Strategy Performance
        strategies = (TradeEntry.objects.filter(user=user).values('strategy').annotate(
            total=Count('id'),
            wins=Count('id', filter=Q(result__gt=0)),
        ).annotate(
            win_rate=ExpressionWrapper(
                100.0 * F('wins') / F('total'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        ))

        strategy_usage = TradeEntry.objects.filter(user=user).values('strategy').annotate(
            count=Count('strategy')
        ).order_by('-count')

        trade_period_data = TradeEntry.objects.filter(user=user).values('trade_period').annotate(
            wins=Count('id', filter=Q(result__gt=0)),
            losses=Count('id', filter=Q(result__lt=0))
        ).order_by('trade_period')

        # Strategy Charts
        strats = [s['strategy'] for s in strategies]
        win_rates = [s['win_rate'] for s in strategies]
        strategy_count = [s['count'] for s in strategy_usage]

        # Time of Day
        period_labels = [p['trade_period'] for p in trade_period_data]
        period_wins = [p['wins'] for p in trade_period_data]
        period_losses = [p['losses'] for p in trade_period_data]

        context = {
            'profit': profit,
            'dates': dates,
            'strats': strats,
            'win_rates': win_rates,
            'strategy_count': strategy_count,
            'period_labels': period_labels,
            'period_wins': period_wins,
            'period_losses': period_losses,
        }

        return render(request, 'journal/analysis.html', context)
    else:
        return redirect('login')


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