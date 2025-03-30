from django import forms
from .models import TradeEntry


class TradeEntryForm(forms.ModelForm):
    class Meta:
        model = TradeEntry
        fields = '__all__'
        exclude = ['user', 'date', 'time', 'result']

    comments = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False)

