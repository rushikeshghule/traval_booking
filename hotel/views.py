from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone

from .models import Hotel, Room, RoomType, HotelBooking

import random
import string
import datetime
import json

# Create your views here.
class HotelSearchView(View):
    """View for searching hotels"""
    template_name = 'hotel/search.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        # Process the search form data
        destination = request.POST.get('destination')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        guests = request.POST.get('guests', 1)
        rooms = request.POST.get('rooms', 1)
        
        # Store search parameters in session
        search_params = {
            'destination': destination,
            'check_in': check_in,
            'check_out': check_out,
            'guests': int(guests),
            'rooms': int(rooms),
        }
        
        request.session['hotel_search'] = search_params
        return redirect('hotel:results')
        
class HotelResultsView(View):
    """View for displaying hotel search results"""
    template_name = 'hotel/results.html'
    
    def get(self, request):
        # Get search parameters from session
        search_params = request.session.get('hotel_search', {})
        
        # Convert string dates to date objects for the template
        if 'check_in' in search_params and search_params['check_in']:
            try:
                search_params['check_in'] = datetime.datetime.strptime(search_params['check_in'], '%Y-%m-%d').date()
            except ValueError:
                search_params['check_in'] = timezone.now().date()
                
        if 'check_out' in search_params and search_params['check_out']:
            try:
                search_params['check_out'] = datetime.datetime.strptime(search_params['check_out'], '%Y-%m-%d').date()
            except ValueError:
                search_params['check_out'] = timezone.now().date() + datetime.timedelta(days=1)
        
        # Sample hotels data - in a real application, this would come from a database
        hotels = [
            {
                'id': 1,
                'name': 'Grand Hotel',
                'address': '123 Main St, Downtown',
                'star_rating': 5,
                'price_per_night': 200,
                'guest_rating': 9.2,
                'review_count': 1284,
                'free_cancellation': True,
                'amenities': ['wifi', 'pool', 'parking', 'breakfast', 'spa', 'gym'],
                'description': 'Luxurious 5-star hotel in the heart of the city with stunning views and top-notch amenities.',
            },
            {
                'id': 2,
                'name': 'Boutique Inn',
                'address': '456 Park Ave, Midtown',
                'star_rating': 4,
                'price_per_night': 150,
                'guest_rating': 8.7,
                'review_count': 943,
                'free_cancellation': True,
                'amenities': ['wifi', 'breakfast'],
                'description': 'Charming boutique hotel with unique rooms and personalized service.',
            },
            {
                'id': 3,
                'name': 'Budget Suites',
                'address': '789 Broadway, Arts District',
                'star_rating': 3,
                'price_per_night': 85,
                'guest_rating': 7.5,
                'review_count': 651,
                'free_cancellation': False,
                'amenities': ['wifi', 'parking'],
                'description': 'Affordable accommodation with basic amenities in a convenient location.',
            },
        ]
        
        context = {
            'destination': search_params.get('destination', 'Unknown'),
            'check_in': search_params.get('check_in', timezone.now().date()),
            'check_out': search_params.get('check_out', timezone.now().date() + datetime.timedelta(days=1)),
            'guests': search_params.get('guests', 1),
            'rooms': search_params.get('rooms', 1),
            'hotels': hotels,
        }
        
        return render(request, self.template_name, context)

class HotelDetailView(LoginRequiredMixin, DetailView):
    """View for displaying hotel details"""
    model = Hotel
    template_name = 'hotel/detail.html'
    context_object_name = 'hotel'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get search data from session
        search_data = self.request.session.get('hotel_search', {})
        check_in = search_data.get('check_in')
        check_out = search_data.get('check_out')
        guests = search_data.get('guests', 1)
        
        # Get available rooms for the hotel
        available_rooms = []
        if check_in and check_out:
            # Convert string dates to datetime objects
            check_in_date = datetime.datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.datetime.strptime(check_out, '%Y-%m-%d').date()
            
            # Get rooms that are available for the entire period
            available_rooms = self.object.rooms.filter(
                capacity__gte=guests,
                is_active=True
            ).exclude(
                # Exclude rooms that have bookings overlapping with the requested period
                bookings__check_in__lt=check_out_date,
                bookings__check_out__gt=check_in_date,
                bookings__status__in=['confirmed', 'pending']
            )
        
        context.update({
            'available_rooms': available_rooms,
            'check_in': check_in,
            'check_out': check_out,
            'guests': guests,
            'nights': (datetime.datetime.strptime(check_out, '%Y-%m-%d').date() - 
                      datetime.datetime.strptime(check_in, '%Y-%m-%d').date()).days if check_in and check_out else 0,
        })
        
        return context

class HotelBookingView(LoginRequiredMixin, View):
    """View for processing hotel booking"""
    def post(self, request, pk):
        # Process booking form
        
        # Redirect to confirmation page
        return redirect('hotel:booking_confirm', pk=pk)

class HotelBookingConfirmView(LoginRequiredMixin, View):
    """View for confirming hotel booking details before payment"""
    template_name = 'hotel/confirmation.html'
    
    def get(self, request, pk):
        # hotel = get_object_or_404(Hotel, pk=pk)
        # room = get_object_or_404(Room, pk=request.session.get('room_id'))
        
        context = {
            # 'hotel': hotel,
            # 'room': room,
            # 'booking_id': ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
            # Additional context data
        }
        
        return render(request, self.template_name, context)

class HotelBookingSuccessView(LoginRequiredMixin, TemplateView):
    """View for displaying booking success page"""
    template_name = 'hotel/success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reference = kwargs.get('reference')
        # booking = get_object_or_404(HotelBooking, reference=reference)
        # context['booking'] = booking
        return context
