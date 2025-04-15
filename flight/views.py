from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.forms import formset_factory
import uuid
import datetime

from .models import Airport, Flight, FlightSeat, FlightBooking, Passenger
from .forms import FlightSearchForm, FlightBookingForm, PassengerForm

class FlightSearchView(View):
    """View for searching flights"""
    
    def get(self, request):
        form = FlightSearchForm()
        return render(request, 'flight/search.html', {'form': form})
    
    def post(self, request):
        form = FlightSearchForm(request.POST)
        if form.is_valid():
            source = form.cleaned_data['source']
            destination = form.cleaned_data['destination']
            departure_date = form.cleaned_data['departure_date']
            return_date = form.cleaned_data['return_date']
            passengers = form.cleaned_data['passengers']
            travel_class = form.cleaned_data['travel_class']
            
            # Store search data in session
            request.session['flight_search'] = {
                'source': source,
                'destination': destination,
                'departure_date': departure_date.strftime('%Y-%m-%d'),
                'return_date': return_date.strftime('%Y-%m-%d') if return_date else None,
                'passengers': passengers,
                'travel_class': travel_class,
                'trip_type': 'round_trip' if return_date else 'one_way',
            }
            
            return redirect('flight:results')
        
        return render(request, 'flight/search.html', {'form': form})

class FlightResultsView(View):
    """View for displaying flight search results"""
    
    def get(self, request):
        # Check if search data exists in session
        search_data = request.session.get('flight_search')
        if not search_data:
            messages.error(request, 'Please search for flights first.')
            return redirect('flight:search')
        
        source = search_data['source']
        destination = search_data['destination']
        departure_date_str = search_data['departure_date']
        return_date_str = search_data['return_date']
        passengers = search_data['passengers']
        travel_class = search_data['travel_class']
        trip_type = search_data['trip_type']
        
        # Convert date strings to datetime
        departure_date = datetime.datetime.strptime(departure_date_str, '%Y-%m-%d').date()
        return_date = datetime.datetime.strptime(return_date_str, '%Y-%m-%d').date() if return_date_str else None
        
        # Get source and destination airports
        source_airports = Airport.objects.filter(
            Q(name__icontains=source) | Q(code__icontains=source) | Q(city__icontains=source)
        )
        destination_airports = Airport.objects.filter(
            Q(name__icontains=destination) | Q(code__icontains=destination) | Q(city__icontains=destination)
        )
        
        # Get outbound flights
        outbound_flights = Flight.objects.filter(
            source__in=source_airports,
            destination__in=destination_airports,
            departure_time__date=departure_date,
            available_seats__gte=passengers
        ).order_by('departure_time')
        
        # Get return flights if round trip
        return_flights = None
        if trip_type == 'round_trip' and return_date:
            return_flights = Flight.objects.filter(
                source__in=destination_airports,
                destination__in=source_airports,
                departure_time__date=return_date,
                available_seats__gte=passengers
            ).order_by('departure_time')
        
        context = {
            'outbound_flights': outbound_flights,
            'return_flights': return_flights,
            'source': source,
            'destination': destination,
            'departure_date': departure_date,
            'return_date': return_date,
            'passengers': passengers,
            'travel_class': travel_class,
            'trip_type': trip_type,
        }
        
        return render(request, 'flight/results.html', context)

class FlightDetailView(LoginRequiredMixin, DetailView):
    """View for displaying flight details"""
    model = Flight
    template_name = 'flight/detail.html'
    context_object_name = 'flight'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flight = self.object
        travel_class = self.request.session.get('flight_search', {}).get('travel_class', 'economy')
        
        # Get available seats for the selected class
        available_seats = FlightSeat.objects.filter(
            flight=flight,
            seat_class=travel_class,
            status='available'
        )
        
        context['available_seats'] = available_seats
        context['travel_class'] = travel_class
        context['passengers'] = self.request.session.get('flight_search', {}).get('passengers', 1)
        
        return context

class FlightBookingView(LoginRequiredMixin, View):
    """View for creating a flight booking"""
    
    def get(self, request, pk):
        flight = get_object_or_404(Flight, pk=pk)
        search_data = request.session.get('flight_search')
        
        if not search_data:
            messages.error(request, 'Please search for flights first.')
            return redirect('flight:search')
        
        passengers = int(search_data['passengers'])
        travel_class = search_data['travel_class']
        
        # Check if enough seats are available
        available_seats = FlightSeat.objects.filter(
            flight=flight,
            seat_class=travel_class,
            status='available'
        )
        
        if available_seats.count() < passengers:
            messages.error(request, f'Not enough seats available. Only {available_seats.count()} seats left.')
            return redirect('flight:detail', pk=pk)
        
        # Create passenger formset
        PassengerFormSet = formset_factory(PassengerForm, extra=passengers)
        formset = PassengerFormSet()
        form = FlightBookingForm()
        
        # Calculate total price based on seat class and passengers
        seat_price = available_seats.first().price
        total_price = seat_price * passengers
        
        context = {
            'flight': flight,
            'form': form,
            'formset': formset,
            'available_seats': available_seats[:passengers],
            'passengers': passengers,
            'travel_class': travel_class,
            'seat_price': seat_price,
            'total_price': total_price,
        }
        
        return render(request, 'flight/booking.html', context)
    
    def post(self, request, pk):
        flight = get_object_or_404(Flight, pk=pk)
        search_data = request.session.get('flight_search')
        
        if not search_data:
            messages.error(request, 'Please search for flights first.')
            return redirect('flight:search')
        
        passengers = int(search_data['passengers'])
        travel_class = search_data['travel_class']
        
        # Validate passenger forms
        PassengerFormSet = formset_factory(PassengerForm, extra=passengers)
        formset = PassengerFormSet(request.POST)
        form = FlightBookingForm(request.POST)
        
        if form.is_valid() and formset.is_valid():
            # Generate reference
            reference = f"FLT-{uuid.uuid4().hex[:8].upper()}"
            
            # Calculate total price
            seat_price = FlightSeat.objects.filter(
                flight=flight,
                seat_class=travel_class,
                status='available'
            ).first().price
            total_price = seat_price * passengers
            
            # Create booking
            booking = FlightBooking(
                user=request.user,
                flight=flight,
                passenger_count=passengers,
                total_price=total_price,
                booking_reference=reference,
                status='pending',
                payment_status='pending',
            )
            booking.save()
            
            # Reserve seats
            seat_ids = request.POST.getlist('seats')
            if seat_ids:
                seats = FlightSeat.objects.filter(id__in=seat_ids)
                booking.seats.add(*seats)
                
                # Update seat status
                for seat in seats:
                    seat.status = 'booked'
                    seat.save()
            
            # Save passenger info
            for i, passenger_form in enumerate(formset):
                if passenger_form.is_valid():
                    passenger = passenger_form.save(commit=False)
                    passenger.booking = booking
                    passenger.save()
            
            # Update available seats
            flight.available_seats -= passengers
            flight.save()
            
            return redirect('flight:booking_confirm', pk=booking.pk)
        
        # If form is invalid, show errors
        available_seats = FlightSeat.objects.filter(
            flight=flight,
            seat_class=travel_class,
            status='available'
        )[:passengers]
        
        seat_price = available_seats.first().price if available_seats.exists() else 0
        total_price = seat_price * passengers
        
        context = {
            'flight': flight,
            'form': form,
            'formset': formset,
            'available_seats': available_seats,
            'passengers': passengers,
            'travel_class': travel_class,
            'seat_price': seat_price,
            'total_price': total_price,
        }
        
        return render(request, 'flight/booking.html', context)

class FlightBookingConfirmView(LoginRequiredMixin, DetailView):
    """View for confirming a flight booking"""
    model = FlightBooking
    template_name = 'flight/booking_confirm.html'
    context_object_name = 'booking'
    
    def get_queryset(self):
        return FlightBooking.objects.filter(user=self.request.user)
    
    def post(self, request, pk):
        booking = get_object_or_404(FlightBooking, pk=pk, user=request.user)
        
        # Process payment logic would go here
        
        # Update booking status
        booking.status = 'confirmed'
        booking.payment_status = 'paid'
        booking.save()
        
        messages.success(request, 'Flight booking confirmed successfully!')
        return redirect('flight:booking_success', reference=booking.booking_reference)

class FlightBookingSuccessView(LoginRequiredMixin, TemplateView):
    """View for displaying booking success message"""
    template_name = 'flight/booking_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reference = self.kwargs.get('reference')
        booking = get_object_or_404(FlightBooking, booking_reference=reference, user=self.request.user)
        context['booking'] = booking
        return context
