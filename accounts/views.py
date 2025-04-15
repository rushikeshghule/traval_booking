from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .models import User
from .forms import ProfileForm

# Add redirect function for authentication pages
def redirect_if_authenticated(view_func):
    """
    Decorator to redirect authenticated users away from login/signup pages
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in.')
            return redirect('accounts:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

class DashboardView(LoginRequiredMixin, TemplateView):
    """View for user dashboard"""
    template_name = 'accounts/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get recent bookings
        bus_bookings = user.busbooking_bookings.all().order_by('-booking_date')[:3]
        flight_bookings = user.flightbooking_bookings.all().order_by('-booking_date')[:3]
        train_bookings = user.trainbooking_bookings.all().order_by('-booking_date')[:3]
        hotel_bookings = user.hotelbooking_bookings.all().order_by('-booking_date')[:3]
        
        context.update({
            'bus_bookings': bus_bookings,
            'flight_bookings': flight_bookings,
            'train_bookings': train_bookings,
            'hotel_bookings': hotel_bookings,
        })
        
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    """View for user profile"""
    template_name = 'accounts/profile.html'

class ProfileEditView(LoginRequiredMixin, UpdateView):
    """View for editing user profile"""
    model = User
    form_class = ProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
        
    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully.')
        return super().form_valid(form)

class BookingsView(LoginRequiredMixin, TemplateView):
    """View for displaying user bookings"""
    template_name = 'accounts/bookings.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get all bookings
        bus_bookings = user.busbooking_bookings.all().order_by('-booking_date')
        flight_bookings = user.flightbooking_bookings.all().order_by('-booking_date')
        train_bookings = user.trainbooking_bookings.all().order_by('-booking_date')
        hotel_bookings = user.hotelbooking_bookings.all().order_by('-booking_date')
        
        context.update({
            'bus_bookings': bus_bookings,
            'flight_bookings': flight_bookings,
            'train_bookings': train_bookings,
            'hotel_bookings': hotel_bookings,
        })
        
        return context
