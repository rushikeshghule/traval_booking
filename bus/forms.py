from django import forms
from django.utils import timezone
import datetime
from .models import BusBooking

class BusSearchForm(forms.Form):
    """Form for searching bus schedules"""
    source = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'From (City or Bus Station)'
    }))
    destination = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'To (City or Bus Station)'
    }))
    date = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'class': 'form-control',
        'type': 'date',
        'min': datetime.date.today().strftime('%Y-%m-%d')
    }))
    passengers = forms.IntegerField(required=True, min_value=1, max_value=10, initial=1, widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))
    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        today = timezone.now().date()
        
        if date < today:
            raise forms.ValidationError("You cannot search for buses on a past date.")
        
        return date

class BusBookingForm(forms.ModelForm):
    """Form for creating a bus booking"""
    
    class Meta:
        model = BusBooking
        fields = []  # No fields needed as we handle this in the view
        
    # Add any additional passenger information fields as needed
    passenger_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Passenger Name'
    }))
    passenger_email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Passenger Email'
    }))
    passenger_phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Passenger Phone'
    }))
    special_request = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Any special requests?',
        'rows': 3
    }))
