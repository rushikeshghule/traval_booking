from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
import uuid
import datetime

from .models import BusRoute, BusSchedule, BusBooking, BusSeat
from .forms import BusSearchForm, BusBookingForm

class BusSearchView(View):
    """View for searching bus schedules"""
    
    def get(self, request):
        form = BusSearchForm()
        return render(request, 'bus/search.html', {'form': form})
    
    def post(self, request):
        form = BusSearchForm(request.POST)
        if form.is_valid():
            source = form.cleaned_data['source']
            destination = form.cleaned_data['destination']
            date = form.cleaned_data['date']
            passengers = form.cleaned_data['passengers']
            
            # Store search data in session
            request.session['bus_search'] = {
                'source': source,
                'destination': destination,
                'date': date.strftime('%Y-%m-%d'),
                'passengers': passengers,
            }
            
            return redirect('bus:results')
        
        return render(request, 'bus/search.html', {'form': form})

class BusResultsView(View):
    """View for displaying bus search results"""
    
    def get(self, request):
        # Check if search data exists in session
        search_data = request.session.get('bus_search')
        if not search_data:
            messages.error(request, 'Please search for buses first.')
            return redirect('bus:search')
        
        source = search_data['source']
        destination = search_data['destination']
        date_str = search_data['date']
        passengers = search_data['passengers']
        
        # Convert date string to datetime
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Get routes matching source and destination
        routes = BusRoute.objects.filter(
            Q(source__icontains=source) & Q(destination__icontains=destination)
        )
        
        # Get schedules for these routes on the given date
        schedules = BusSchedule.objects.filter(
            route__in=routes,
            departure_time__date=date,
            available_seats__gte=passengers
        ).order_by('departure_time')
        
        context = {
            'schedules': schedules,
            'source': source,
            'destination': destination,
            'date': date,
            'passengers': passengers,
        }
        
        return render(request, 'bus/results.html', context)

class BusDetailView(LoginRequiredMixin, DetailView):
    """View for displaying bus schedule details"""
    model = BusSchedule
    template_name = 'bus/detail.html'
    context_object_name = 'schedule'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_seats'] = self.object.seats.filter(status='available')
        return context

class BusBookingView(LoginRequiredMixin, View):
    """View for creating a bus booking"""
    
    def get(self, request, pk):
        schedule = get_object_or_404(BusSchedule, pk=pk)
        search_data = request.session.get('bus_search')
        
        if not search_data:
            messages.error(request, 'Please search for buses first.')
            return redirect('bus:search')
        
        passengers = int(search_data['passengers'])
        
        if schedule.available_seats < passengers:
            messages.error(request, f'Not enough seats available. Only {schedule.available_seats} seats left.')
            return redirect('bus:detail', pk=pk)
        
        available_seats = schedule.seats.filter(status='available')[:passengers]
        form = BusBookingForm()
        
        context = {
            'schedule': schedule,
            'form': form,
            'available_seats': available_seats,
            'passengers': passengers,
            'total_price': schedule.fare * passengers,
        }
        
        return render(request, 'bus/booking.html', context)
    
    def post(self, request, pk):
        schedule = get_object_or_404(BusSchedule, pk=pk)
        form = BusBookingForm(request.POST)
        search_data = request.session.get('bus_search')
        
        if not search_data:
            messages.error(request, 'Please search for buses first.')
            return redirect('bus:search')
        
        passengers = int(search_data['passengers'])
        
        if form.is_valid():
            # Generate reference
            reference = f"BUS-{uuid.uuid4().hex[:8].upper()}"
            
            # Create booking
            booking = BusBooking(
                user=request.user,
                schedule=schedule,
                passenger_count=passengers,
                total_price=schedule.fare * passengers,
                booking_reference=reference,
                status='pending',
                payment_status='pending',
            )
            booking.save()
            
            # Reserve seats
            seat_ids = request.POST.getlist('seats')
            seats = BusSeat.objects.filter(id__in=seat_ids)
            booking.seats.add(*seats)
            
            # Update seat status
            for seat in seats:
                seat.status = 'booked'
                seat.save()
            
            # Update available seats
            schedule.available_seats -= passengers
            schedule.save()
            
            return redirect('bus:booking_confirm', pk=booking.pk)
        
        available_seats = schedule.seats.filter(status='available')[:passengers]
        
        context = {
            'schedule': schedule,
            'form': form,
            'available_seats': available_seats,
            'passengers': passengers,
            'total_price': schedule.fare * passengers,
        }
        
        return render(request, 'bus/booking.html', context)

class BusBookingConfirmView(LoginRequiredMixin, DetailView):
    """View for confirming a bus booking"""
    model = BusBooking
    template_name = 'bus/booking_confirm.html'
    context_object_name = 'booking'
    
    def get_queryset(self):
        return BusBooking.objects.filter(user=self.request.user)
    
    def post(self, request, pk):
        booking = get_object_or_404(BusBooking, pk=pk, user=request.user)
        
        # Process payment logic would go here
        
        # Update booking status
        booking.status = 'confirmed'
        booking.payment_status = 'paid'
        booking.save()
        
        messages.success(request, 'Booking confirmed successfully!')
        return redirect('bus:booking_success', reference=booking.booking_reference)

class BusBookingSuccessView(LoginRequiredMixin, TemplateView):
    """View for displaying booking success message"""
    template_name = 'bus/booking_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reference = self.kwargs.get('reference')
        booking = get_object_or_404(BusBooking, booking_reference=reference, user=self.request.user)
        context['booking'] = booking
        return context
