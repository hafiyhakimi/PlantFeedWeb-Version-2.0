from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from oauth2_provider.views.generic import ProtectedResourceView
from member.models import Person
from django.contrib import messages
from oauth2_provider.models import AccessToken, Application
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.db import transaction
from django.contrib.auth import authenticate
from django.utils import timezone
from django.http import HttpResponseRedirect
import logging

@login_required
def custom_oauth_authorization(request):
    # Your custom OAuth2 authorization view logic goes here
    # This view should render a template with user login and consent form
    return render(request, 'custom_oauth_authorization.html')

class CustomProtectedResourceView(ProtectedResourceView):
    # Your custom OAuth2 protected resource view logic goes here

    # Example: Override the dispatch method to add custom behavior
    def dispatch(self, request, *args, **kwargs):
        # Add your custom logic here before accessing protected resources
        # For example, you can perform additional authentication checks
        # or authorization checks here.
        
        # Call the parent class's dispatch method to handle resource access
        return super().dispatch(request, *args, **kwargs)

@transaction.atomic
# def login_view(request):
#     logger = logging.getLogger(__name__)

#     if request.method == "POST":
#         email = request.POST.get('Email')
#         password = request.POST.get('Pwd')

#         # Authenticate user based on Email and Password using authenticate method
#         user = authenticate(request, Email = email, Pass = password)
#         print("User: ", user)

#         if user is not None:
#             # User authentication succeeded
#             auth_login(request, user)

#             # Generate an OAuth2 access token for the user
#             try:
#                 oauth_application = Application.objects.get(client_id='TeoEbwMZQWGf4TGlCbpFmtKxfRyOxS1RCSwV19bH')

#                 # Check if an AccessToken already exists for this user and application
#                 access_token, created = AccessToken.objects.get_or_create(
#                     user=user,
#                     application=oauth_application,
#                     scope='read write',  # Define the appropriate scope
#                 )

#                 # Redirect to the custom OAuth2 authorization view
#                 return render(request, 'custom_oauth_authorization.html', {'access_token': access_token.token})

#             except Application.DoesNotExist:
#                 logger.error("OAuth2 application not found. Contact the administrator.")
#                 return HttpResponse("OAuth2 application not found. Contact the administrator.")

#         else:
#             # User authentication failed
#             messages.error(request, 'Username/Password Invalid..!')

#     return render(request, 'plantlink_login.html')

@transaction.atomic
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('Email')
        password = request.POST.get('Pwd')

        # Authenticate user based on Email and Password
        try:
            user = Person.objects.get(Email=email, Pass=password)
        except Person.DoesNotExist:
            user = None
            
        print("User: ", user)

        if user is not None:
            # User authentication succeeded
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # Generate an OAuth2 access token for the user
            try:
                oauth_application = Application.objects.get(client_id='TeoEbwMZQWGf4TGlCbpFmtKxfRyOxS1RCSwV19bH')
                
                # Calculate the expiration date (one day from now)
                expiration_date = timezone.now() + timezone.timedelta(days=1)
                access_token = AccessToken.objects.create(
                    user=user,
                    application=oauth_application,
                    scope='read write',  # Define the appropriate scope
                    expires=expiration_date,
                )
                
                print("Access Token: ", access_token.token)

                # Redirect to the custom OAuth2 authorization view
                return render(request, 'custom_oauth_authorization.html', {'access_token': access_token.token})

            except Application.DoesNotExist:
                return HttpResponse("OAuth2 application not found. Contact the administrator.")

        else:
            # User authentication failed
            messages.error(request, 'Username/Password Invalid..!')

    return render(request, 'plantlink_login.html')

def token_exchange_view(request):
    # Extract the access token from the query parameters
    access_token = request.GET.get('access_token')

    # Perform any additional processing if needed

    # Redirect to the "PlantLink" URL with the access token as a query parameter
    redirect_url = f'http://plantlink-url.com/?access_token={access_token}'
    return redirect(redirect_url)

def authorize(request):
    # In this view, you can handle the user's authorization decision.
    # You should obtain the access token and any other necessary information
    # from the request and perform the required authorization logic.

    # Example: Retrieving the access token from the query parameter
    access_token = request.GET.get('access_token')

    if access_token:
        # Perform your authorization logic here.
        # This can include validating the token, associating it with a user,
        # and any other checks you need to ensure the user's data is secure.
        print("Access token found")
        # If authorization is successful, you can redirect the user to PlantLink.
        # Replace 'http://plantlink.com' with the actual URL.
        redirect_url = f'http://plantlink.com?access_token={access_token}'
        return HttpResponseRedirect(redirect_url)
    else:
        # Handle the case where the access token is missing or invalid.
        # You might want to display an error message or redirect to an error page.
        print("No access token found")
        return render(request, 'error.html', {'message': 'Authorization failed.'})

def deny(request):
    # In this view, you can handle the user's decision to deny authorization.
    # You can display a message or perform any other actions as needed.

    # Example: Display a denial message.
    return render(request, 'deny.html', {'message': 'Authorization denied.'})
