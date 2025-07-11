from django import forms
from django.utils.timezone import now
from .models import TradeEntry


class TradeEntryForm(forms.ModelForm):
    class Meta:
        model = TradeEntry
        fields = '__all__'
        exclude = ['user', 'result']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'entry_time': forms.TimeInput(attrs={'class': 'flatpickr-time', 'type': 'text'}),
            'exit_time': forms.TimeInput(attrs={'class': 'flatpickr-time', 'type': 'text'}),
        }

    comments = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False)

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=now().date(),
        required=True
    )

