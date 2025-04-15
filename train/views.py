from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone

from .models import Train, TrainBooking, TrainPassenger
from .forms import TrainSearchForm

import random
import string
import datetime
import json

# Create your views here.
class TrainSearchView(View):
    """View for searching trains"""
    template_name = 'train/search.html'
    
    def get(self, request):
        form = TrainSearchForm()
        return render(request, self.template_name, {
            'form': form
        })
    
    def post(self, request):
        form = TrainSearchForm(request.POST)
        if form.is_valid():
            # Store search parameters in session
            cleaned_data = form.cleaned_data.copy()
            
            # Convert date objects to strings to make them JSON serializable
            if 'departure_date' in cleaned_data and isinstance(cleaned_data['departure_date'], datetime.date):
                cleaned_data['departure_date'] = cleaned_data['departure_date'].isoformat()
            
            if 'return_date' in cleaned_data and isinstance(cleaned_data['return_date'], datetime.date):
                cleaned_data['return_date'] = cleaned_data['return_date'].isoformat()
                
            request.session['train_search'] = cleaned_data
            return redirect('train:results')
        return render(request, self.template_name, {'form': form})

class TrainResultsView(View):
    """View for displaying train search results"""
    template_name = 'train/results.html'
    
    def get(self, request):
        # Get search parameters from session
        search_params = request.session.get('train_search', {})
        
        # Convert string dates back to date objects for the template
        if 'departure_date' in search_params and isinstance(search_params['departure_date'], str):
            search_params['departure_date'] = datetime.date.fromisoformat(search_params['departure_date'])
            
        if 'return_date' in search_params and isinstance(search_params['return_date'], str):
            search_params['return_date'] = datetime.date.fromisoformat(search_params['return_date'])
        
        context = {
            'source': search_params.get('source', 'New York'),
            'destination': search_params.get('destination', 'Boston'),
            'departure_date': search_params.get('departure_date', timezone.now().date()),
            'return_date': search_params.get('return_date'),
            'passengers': search_params.get('passengers', 1),
            'train_class': search_params.get('train_class', 'economy'),
            'outbound_trains': [],  # Placeholder
            'return_trains': [],  # Placeholder
            'journey_type': search_params.get('journey_type', 'one_way'),
        }
        
        return render(request, self.template_name, context)

class TrainDetailView(LoginRequiredMixin, DetailView):
    """View for displaying train details and booking form"""
    template_name = 'train/detail.html'
    model = Train
    context_object_name = 'train'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Additional context data
        context['passengers'] = 1  # Placeholder
        context['train_class'] = 'economy'  # Placeholder
        context['passenger_range'] = range(1, 2)  # Placeholder
        context['base_total'] = 100  # Placeholder
        context['taxes'] = 20  # Placeholder
        context['total_price'] = 120  # Placeholder
        return context

class TrainBookingView(LoginRequiredMixin, View):
    """View for processing train booking"""
    def post(self, request, pk):
        # Process booking form
        
        # Redirect to confirmation page
        return redirect('train:booking_confirm', pk=pk)

class TrainBookingConfirmView(LoginRequiredMixin, View):
    """View for confirming train booking details before payment"""
    template_name = 'train/confirmation.html'
    
    def get(self, request, pk):
        # train = get_object_or_404(Train, pk=pk)
        
        context = {
            # 'train': train,
            # 'booking_id': ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
            # Additional context data
        }
        
        return render(request, self.template_name, context)

class TrainBookingSuccessView(LoginRequiredMixin, TemplateView):
    """View for displaying booking success page"""
    template_name = 'train/success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reference = kwargs.get('reference')
        # booking = get_object_or_404(TrainBooking, reference=reference)
        # context['booking'] = booking
        return context
