from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseBooking
import uuid

# Create your models here.

class BusOperator(models.Model):
    """Model for bus operators/companies"""
    
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='bus_operators', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class BusRoute(models.Model):
    """Model for bus routes"""
    
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    distance = models.DecimalField(max_digits=10, decimal_places=2, help_text="Distance in kilometers")
    duration = models.DurationField(help_text="Expected journey duration")
    
    def __str__(self):
        return f"{self.source} to {self.destination}"
        
    class Meta:
        unique_together = ['source', 'destination']

class Bus(models.Model):
    """Model for buses"""
    
    BUS_TYPE_CHOICES = (
        ('normal', _('Normal')),
        ('ac', _('AC')),
        ('sleeper', _('Sleeper')),
        ('luxury', _('Luxury')),
    )
    
    operator = models.ForeignKey(BusOperator, on_delete=models.CASCADE, related_name='buses')
    bus_number = models.CharField(max_length=20)
    bus_type = models.CharField(max_length=20, choices=BUS_TYPE_CHOICES)
    total_seats = models.PositiveIntegerField()
    amenities = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.bus_number} - {self.operator.name} ({self.get_bus_type_display()})"

class BusSchedule(models.Model):
    """Model for bus schedules"""
    
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='schedules')
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE, related_name='schedules')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.bus.bus_number} - {self.route} - {self.departure_time}"

class BusSeat(models.Model):
    """Model for individual bus seats"""
    
    SEAT_TYPE_CHOICES = (
        ('window', _('Window')),
        ('aisle', _('Aisle')),
        ('middle', _('Middle')),
    )
    
    SEAT_STATUS_CHOICES = (
        ('available', _('Available')),
        ('booked', _('Booked')),
        ('reserved', _('Reserved')),
        ('unavailable', _('Unavailable')),
    )
    
    schedule = models.ForeignKey(BusSchedule, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    seat_type = models.CharField(max_length=20, choices=SEAT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=SEAT_STATUS_CHOICES, default='available')
    
    def __str__(self):
        return f"{self.seat_number} - {self.schedule.bus.bus_number}"
        
    class Meta:
        unique_together = ['schedule', 'seat_number']

class BusBooking(BaseBooking):
    """Model for bus bookings"""
    
    schedule = models.ForeignKey(BusSchedule, on_delete=models.CASCADE, related_name='bookings')
    seats = models.ManyToManyField(BusSeat, related_name='bookings')
    passenger_count = models.PositiveIntegerField()
    
    def save(self, *args, **kwargs):
        # Generate unique booking reference if not provided
        if not self.booking_reference:
            self.booking_reference = f"BUS-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.booking_reference} - {self.schedule.route}"
