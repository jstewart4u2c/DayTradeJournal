from django import forms
from .models import TradeEntry


class TradeEntryForm(forms.ModelForm):
    class Meta:
        model = TradeEntry
        fields = '__all__'
        exclude = ['date', 'time', 'result']

