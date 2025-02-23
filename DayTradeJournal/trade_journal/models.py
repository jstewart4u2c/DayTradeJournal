from django.conf import settings
from django.db import models
from django import forms


# Create your models here.
class TradeEntry(models.Model):
    trade_period_choices = [
        ('Pre-Market', 'Pre-Market'),
        ('Intraday', 'Intraday'),
        ('After Hours', 'After Hours'),
    ]

    strategy_choices = [
        ('breakout', 'Breakout'),
        ('dip buy', 'Dip Buy'),
        ('gap up', 'Gap Up'),
        ('gap down', 'Gap Down'),
        ('short sell', 'Short Sell'),
        ('supernova', 'Supernova'),
        ('swing trade', 'Swing Trade'),
    ]

    # Framework choices are 1-7
    framework_choices = [(i, str(i)) for i in range(1, 8)]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    ticker = models.CharField(max_length=8)
    float = models.CharField(max_length=10)
    trade_period = models.CharField(max_length=50, choices=trade_period_choices)
    strategy = models.CharField(max_length=50, choices=strategy_choices)
    framework = models.PositiveIntegerField(choices=framework_choices, default=1)
    entry_price = models.DecimalField(max_digits=10, decimal_places=2)
    exit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField()
    result = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)


