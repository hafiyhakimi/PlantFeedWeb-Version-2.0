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
from django.views.decorators.csrf import csrf_exempt

import random
import string
from datetime import timedelta
from django.utils import timezone
#from myapp.models import AccessToken

def generate_access_token(length=10):
    # Define the characters to use for generating the token
    characters = string.ascii_uppercase + string.digits

    # Generate a random token by selecting characters randomly
    token = ''.join(random.choice(characters) for _ in range(length))

    return token

@login_required
def custom_oauth_authorization(request):
    return render(request, 'custom_oauth_authorization.html')

class CustomProtectedResourceView(ProtectedResourceView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

@csrf_exempt
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

            # Generate a random access token
            access_token_string = generate_access_token(length=10)
                
            expiration_date = timezone.now() + timezone.timedelta(days=1)
            access_token = AccessToken.objects.create(
                user=user,
                token=access_token_string,
                scope='read write',
                expires=expiration_date,
            )
                
            print("Access Token: ", access_token)

            return render(request, 'custom_oauth_authorization.html', {'access_token': access_token})

        else:
            messages.error(request, 'Username/Password Invalid..!')

    return render(request, 'plantlink_login.html')

def token_exchange_view(request):
    access_token = request.GET.get('access_token')

    redirect_url = f'http://plantlink-url.com/?access_token={access_token}'
    return redirect(redirect_url)

# def authorize(request):
#     access_token = request.GET.get('access_token')

#     if access_token:
#         print("Access token found")
#         redirect_url = f'https://www.google.com/?access_token={access_token}'
#         return HttpResponseRedirect(redirect_url)
#     else:
#         print("No access token found")
#         return render(request, 'error.html')

@csrf_exempt
def authorize(request):
    access_token = request.POST.get('access_token')
    print("Access token found:", access_token)
    if access_token:
        print("Access token found:", access_token)
        # Construct the redirect URL with the access_token parameter
        redirect_url = f'https://www.google.com/?access_token={access_token}'
        return HttpResponseRedirect(redirect_url)
    else:
        print("No access token found")
        return render(request, 'error.html')


def deny(request):
    messages.success(request,'Authorization Denied..!')
    return render(request, 'plantlink_login.html')

@login_required
def user_data_api(request):
    user = request.user
    user_data = {
        'email': user.Email,
        'username': user.Username,
    }
    
    # Return the user data as a JSON response.
    return JsonResponse(user_data)
