from django.shortcuts import redirect
from django.urls import reverse

class AdminOnlyMiddleware:
    """
    Middleware to ensure only admins can access the /users/ URL.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    
    def __call__(self, request):
        # Check if the user is logged in by verifying the session
        user = request.session.get('user')       
        # Define restricted paths
        # restricted_paths = ['/users/', '/index/']

        if request.path.startswith('/users/'):
            if not user:  # If no user in session, redirect to login
                return redirect(reverse('login'))
            if user.get('role') != 'Admin':  # If user is not an admin, redirect to permission denied
                return redirect('permission_denied')

        return self.get_response(request)