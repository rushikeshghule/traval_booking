from django import forms
from django.utils import timezone
import datetime
from .models import FlightBooking, Passenger

class FlightSearchForm(forms.Form):
    """Form for searching flights"""
    source = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'From (City or Airport)'
    }))
    destination = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'To (City or Airport)'
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
    travel_class = forms.ChoiceField(required=True, choices=(
        ('economy', 'Economy'),
        ('premium_economy', 'Premium Economy'),
        ('business', 'Business'),
        ('first', 'First Class')
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

class PassengerForm(forms.ModelForm):
    """Form for passenger details"""
    class Meta:
        model = Passenger
        fields = ['first_name', 'last_name', 'email', 'phone', 'passport_number', 'date_of_birth']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class FlightBookingForm(forms.ModelForm):
    """Form for creating a flight booking"""
    class Meta:
        model = FlightBooking
        fields = []  # We'll handle the fields in the view
        
    # Additional fields
    special_requests = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Any special requests?',
        'rows': 3
    }))
    contact_email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Contact Email'
    }))
    contact_phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Contact Phone'
    }))
