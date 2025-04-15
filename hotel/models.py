from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseBooking
import uuid

# Create your models here.

class HotelChain(models.Model):
    """Model for hotel chains"""
    
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='hotel_chains', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Hotel(models.Model):
    """Model for hotels"""
    
    HOTEL_RATING_CHOICES = (
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    )
    
    chain = models.ForeignKey(HotelChain, on_delete=models.CASCADE, related_name='hotels', null=True, blank=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    star_rating = models.PositiveSmallIntegerField(choices=HOTEL_RATING_CHOICES)
    description = models.TextField()
    amenities = models.TextField(blank=True, null=True)
    check_in_time = models.TimeField(default='14:00')
    check_out_time = models.TimeField(default='11:00')
    image = models.ImageField(upload_to='hotels', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.city}, {self.country}"

class RoomType(models.Model):
    """Model for hotel room types"""
    
    ROOM_TYPE_CHOICES = (
        ('single', _('Single')),
        ('double', _('Double')),
        ('twin', _('Twin')),
        ('deluxe', _('Deluxe')),
        ('suite', _('Suite')),
        ('presidential', _('Presidential Suite')),
        ('family', _('Family Room')),
    )
    
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveSmallIntegerField(help_text="Maximum number of guests")
    amenities = models.TextField(blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True, help_text="Room size in square meters/feet")
    image = models.ImageField(upload_to='room_types', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.hotel.name}"
        
    class Meta:
        unique_together = ['hotel', 'name']

class Room(models.Model):
    """Model for individual hotel rooms"""
    
    ROOM_STATUS_CHOICES = (
        ('available', _('Available')),
        ('occupied', _('Occupied')),
        ('maintenance', _('Under Maintenance')),
        ('reserved', _('Reserved')),
    )
    
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    floor = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=ROOM_STATUS_CHOICES, default='available')
    
    def __str__(self):
        return f"Room {self.room_number} - {self.room_type.name} - {self.hotel.name}"
        
    class Meta:
        unique_together = ['hotel', 'room_number']

class HotelBooking(BaseBooking):
    """Model for hotel bookings"""
    
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='bookings')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='bookings')
    rooms = models.ManyToManyField(Room, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guest_count = models.PositiveSmallIntegerField()
    special_requests = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Generate unique booking reference if not provided
        if not self.booking_reference:
            self.booking_reference = f"HTL-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.booking_reference} - {self.hotel.name} ({self.check_in_date} to {self.check_out_date})"
        
    @property
    def nights(self):
        """Calculate the number of nights for the booking"""
        return (self.check_out_date - self.check_in_date).days

class HotelGuest(models.Model):
    """Model for hotel guests"""
    
    booking = models.ForeignKey(HotelBooking, on_delete=models.CASCADE, related_name='guests')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    id_type = models.CharField(max_length=50, blank=True, null=True)
    id_number = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
