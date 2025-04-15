from django import forms
from django.utils import timezone
import datetime
from .models import TrainBooking

class TrainSearchForm(forms.Form):
    """Form for searching trains"""
    source = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'From (City or Station)'
    }))
    destination = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'To (City or Station)'
    }))
    departure_date = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'class': 'form-control',
        'type': 'date',
        'min': datetime.date.today().strftime('%Y-%m-%d')
    }))
    return_date = forms.DateField(required=False, widget=forms.DateInput(attrs={
        'class': 'form-control',
        'type': 'date',
        'min': datetime.date.today().strftime('%Y-%m-%d')
    }))
    passengers = forms.IntegerField(required=True, min_value=1, max_value=10, initial=1, widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))
    train_class = forms.ChoiceField(required=True, choices=(
        ('economy', 'Economy'),
        ('business', 'Business'),
        ('first', 'First Class'),
        ('sleeper', 'Sleeper')
    ), widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    
    def clean(self):
        cleaned_data = super().clean()
        departure_date = cleaned_data.get('departure_date')
        return_date = cleaned_data.get('return_date')
        today = timezone.now().date()
        
        if departure_date and departure_date < today:
            raise forms.ValidationError("Departure date cannot be in the past.")
        
        if return_date and return_date < departure_date:
            raise forms.ValidationError("Return date cannot be before departure date.")
        
        return cleaned_data
