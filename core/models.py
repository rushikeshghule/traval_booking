from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User

# Create your models here.

class BaseBooking(models.Model):
    """Base model for all booking types"""
    
    BOOKING_STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('cancelled', _('Cancelled')),
        ('completed', _('Completed')),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('paid', _('Paid')),
        ('refunded', _('Refunded')),
        ('failed', _('Failed')),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_reference = models.CharField(max_length=20, unique=True)
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return f"{self.booking_reference} - {self.user.email}"
