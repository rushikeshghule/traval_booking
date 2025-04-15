from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Create your views here.

class HomeView(TemplateView):
    """View for the home page"""
    template_name = 'core/home.html'

class AboutView(TemplateView):
    """View for the about page"""
    template_name = 'core/about.html'

class ContactView(View):
    """View for the contact page"""
    def get(self, request):
        return render(request, 'core/contact.html')
        
    def post(self, request):
        # Process contact form
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you would typically send an email or save to database
        
        messages.success(request, 'Your message has been sent successfully. We will get back to you soon!')
        return redirect('contact')

class FAQView(TemplateView):
    """View for the FAQ page"""
    template_name = 'core/faq.html'

class TermsView(TemplateView):
    """View for the terms and conditions page"""
    template_name = 'core/terms.html'

class PrivacyView(TemplateView):
    """View for the privacy policy page"""
    template_name = 'core/privacy.html'
