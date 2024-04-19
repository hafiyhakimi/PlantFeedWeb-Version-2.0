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
from django.http import JsonResponse
import logging

@login_required
def custom_oauth_authorization(request):
    return render(request, 'custom_oauth_authorization.html')

class CustomProtectedResourceView(ProtectedResourceView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

@transaction.atomic
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('Email')
        password = request.POST.get('Pwd')

        try:
            user = Person.objects.get(Email=email, Pass=password)
        except Person.DoesNotExist:
            user = None
            
        print("User: ", user)

        if user is not None:
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            try:
                oauth_application = Application.objects.get(client_id='TeoEbwMZQWGf4TGlCbpFmtKxfRyOxS1RCSwV19bH')
                
                expiration_date = timezone.now() + timezone.timedelta(days=1)
                access_token = AccessToken.objects.create(
                    user=user,
                    application=oauth_application,
                    scope='read write',
                    expires=expiration_date,
                )
                
                print("Access Token: ", access_token.token)

                return render(request, 'custom_oauth_authorization.html', {'access_token': access_token.token})

            except Application.DoesNotExist:
                return HttpResponse("OAuth2 application not found. Contact the administrator.")

        else:
            messages.error(request, 'Username/Password Invalid..!')

    return render(request, 'plantlink_login.html')

def token_exchange_view(request):
    access_token = request.GET.get('access_token')

    redirect_url = f'http://plantlink-url.com/?access_token={access_token}'
    return redirect(redirect_url)

def authorize(request):
    access_token = request.GET.get('access_token')

    if access_token:
        print("Access token found")
        redirect_url = f'http://plantlink.com?access_token={access_token}'
        return HttpResponseRedirect(redirect_url)
    else:
        print("No access token found")
        return render(request, 'error.html', {'message': 'Authorization failed.'})

def deny(request):
    return render(request, 'deny.html', {'message': 'Authorization denied.'})

@login_required
def user_data_api(request):
    user = request.user
    user_data = {
        'email': user.Email,
        'username': user.Username,
    }
    
    # Return the user data as a JSON response.
    return JsonResponse(user_data)
