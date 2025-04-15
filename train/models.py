from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseBooking
import uuid

# Create your models here.

class TrainOperator(models.Model):
    """Model for train operators/companies"""
    
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='train_operators', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Station(models.Model):
    """Model for train stations"""
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.code}), {self.city}"

class Train(models.Model):
    """Model for trains"""
    
    TRAIN_TYPE_CHOICES = (
        ('express', _('Express')),
        ('passenger', _('Passenger')),
        ('superfast', _('Superfast')),
        ('luxury', _('Luxury')),
    )
    
    operator = models.ForeignKey(TrainOperator, on_delete=models.CASCADE, related_name='trains')
    train_number = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    train_type = models.CharField(max_length=20, choices=TRAIN_TYPE_CHOICES)
    
    def __str__(self):
        return f"{self.train_number} - {self.name}"

class TrainRoute(models.Model):
    """Model for train routes"""
    
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='routes')
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='departures')
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='arrivals')
    distance = models.DecimalField(max_digits=10, decimal_places=2, help_text="Distance in kilometers")
    duration = models.DurationField(help_text="Expected journey duration")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    
    def __str__(self):
        return f"{self.train.name} - {self.source.name} to {self.destination.name}"

class TrainClass(models.Model):
    """Model for train classes"""
    
    CLASS_TYPE_CHOICES = (
        ('SL', _('Sleeper')),
        ('3A', _('AC 3 Tier')),
        ('2A', _('AC 2 Tier')),
        ('1A', _('AC First Class')),
        ('CC', _('Chair Car')),
        ('EC', _('Executive Chair Car')),
        ('GN', _('General')),
    )
    
    train_route = models.ForeignKey(TrainRoute, on_delete=models.CASCADE, related_name='classes')
    class_type = models.CharField(max_length=5, choices=CLASS_TYPE_CHOICES)
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.get_class_type_display()} - {self.train_route.train.name}"
        
    class Meta:
        verbose_name_plural = "Train Classes"

class TrainBooking(BaseBooking):
    """Model for train bookings"""
    
    train_route = models.ForeignKey(TrainRoute, on_delete=models.CASCADE, related_name='bookings')
    train_class = models.ForeignKey(TrainClass, on_delete=models.CASCADE, related_name='bookings')
    travel_date = models.DateField()
    seat_numbers = models.CharField(max_length=255, blank=True, null=True)
    passenger_count = models.PositiveIntegerField()
    
    def save(self, *args, **kwargs):
        # Generate unique booking reference if not provided
        if not self.booking_reference:
            self.booking_reference = f"TRN-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.booking_reference} - {self.train_route}"

class TrainPassenger(models.Model):
    """Model for train passengers"""
    
    booking = models.ForeignKey(TrainBooking, on_delete=models.CASCADE, related_name='passengers')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    id_proof = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
