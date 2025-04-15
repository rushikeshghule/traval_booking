from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class AuthRequiredMiddleware:
    """
    Middleware to require authentication for all pages except a whitelist
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Define URLs that don't require authentication
        self.public_urls = [
            '/account/login/',
            '/accounts/login/',
            '/account/signup/',
            '/accounts/signup/',
            '/accounts/password/reset/',
            '/admin/login/',
            '/static/',
            '/media/',
        ]

    def __call__(self, request):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            # Allow access to whitelisted URLs
            current_path = request.path
            
            # Check if current path is in public URLs
            if not any(current_path.startswith(url) for url in self.public_urls):
                # Store the current URL for redirect after login
                next_url = request.get_full_path()
                request.session['next'] = next_url
                
                # Redirect to login page with a message
                messages.warning(request, 'Please log in to access this page.')
                return redirect(f"{reverse('account_login')}?next={next_url}")
        
        # Process the request for authenticated users or public URLs
        response = self.get_response(request)
        return response 