from datetime import timezone

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
        ('Breakout', 'Breakout'),
        ('Dip Buy', 'Dip Buy'),
        ('Gap Up', 'Gap Up'),
        ('Gap Down', 'Gap Down'),
        ('Short Sell', 'Short Sell'),
        ('Supernova', 'Supernova'),
        ('Swing Trade', 'Swing Trade'),
    ]

    sector_choices = [
        ('No Sector', 'No Sector'),
        ('Media', 'Media'),
        ('Technology', 'Technology'),
        ('Real Estate', 'Real Estate'),
        ('Finance', 'Finance'),
        ('Utilities', 'Utilities'),
        ('Healthcare', 'Healthcare'),
        ('Materials', 'Materials'),
        ('Industrials', 'Industrials'),
        ('Consumer Discretionary', 'Consumer Discretionary'),
        ('Consumer Staples', 'Consumer Staples'),
        ('Energy', 'Energy'),
    ]

    # Framework choices are 1-7
    framework_choices = [(i, str(i)) for i in range(1, 8)]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    ticker = models.CharField(max_length=8)
    sector = models.CharField(max_length=50, choices=sector_choices, default='No Sector')
    float = models.CharField(max_length=10)
    trade_period = models.CharField(max_length=50, choices=trade_period_choices)
    framework = models.PositiveIntegerField(choices=framework_choices, default=1)
    strategy = models.CharField(max_length=50, choices=strategy_choices)
    entry_price = models.DecimalField(max_digits=10, decimal_places=2)
    exit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField()
    result = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    # Auto result calculation using the trade entry and exit prices
    def calculate_result(self):
        if self.exit_price is not None:
            return (self.exit_price - self.entry_price) * self.quantity
        return None

    # Save method override to calculate result using above method
    def save(self, *args, **kwargs):
        self.result = self.calculate_result()
        super().save(*args, **kwargs)

