from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseBooking
import uuid

# Create your models here.

class Airline(models.Model):
    """Model for airlines"""
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    logo = models.ImageField(upload_to='airlines', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class Airport(models.Model):
    """Model for airports"""
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.code}), {self.city}"

class Flight(models.Model):
    """Model for flights"""
    
    FLIGHT_TYPE_CHOICES = (
        ('domestic', _('Domestic')),
        ('international', _('International')),
    )
    
    FLIGHT_CLASS_CHOICES = (
        ('economy', _('Economy')),
        ('premium_economy', _('Premium Economy')),
        ('business', _('Business')),
        ('first', _('First Class')),
    )
    
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='flights')
    flight_number = models.CharField(max_length=20)
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departures')
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivals')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    duration = models.DurationField(null=True, blank=True)
    flight_type = models.CharField(max_length=20, choices=FLIGHT_TYPE_CHOICES)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    aircraft_type = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.airline.code}{self.flight_number} - {self.source.code} to {self.destination.code}"

class FlightSeat(models.Model):
    """Model for individual flight seats"""
    
    SEAT_STATUS_CHOICES = (
        ('available', _('Available')),
        ('booked', _('Booked')),
        ('reserved', _('Reserved')),
        ('unavailable', _('Unavailable')),
    )
    
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    seat_class = models.CharField(max_length=20, choices=Flight.FLIGHT_CLASS_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=SEAT_STATUS_CHOICES, default='available')
    
    def __str__(self):
        return f"{self.seat_number} ({self.get_seat_class_display()}) - {self.flight.flight_number}"
        
    class Meta:
        unique_together = ['flight', 'seat_number']

class FlightBooking(BaseBooking):
    """Model for flight bookings"""
    
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='bookings')
    seats = models.ManyToManyField(FlightSeat, related_name='bookings')
    passenger_count = models.PositiveIntegerField()
    
    def save(self, *args, **kwargs):
        # Generate unique booking reference if not provided
        if not self.booking_reference:
            self.booking_reference = f"FLT-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.booking_reference} - {self.flight}"

class Passenger(models.Model):
    """Model for flight passengers"""
    
    booking = models.ForeignKey(FlightBooking, on_delete=models.CASCADE, related_name='passengers')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    passport_number = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
