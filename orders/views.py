from django.shortcuts import render
from django.http.response import Http404
from django.shortcuts import render, redirect, get_object_or_404
# from LOGIN.models import Person as FarmingPerson
# from LOGIN.models import Feed, Booking, Workshop, Group, Member 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
# from .forms import CreateInDiscussion, PersonForm, UserUpdateForm
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save
from django.dispatch import receiver
from cryptography.fernet import Fernet
from django.conf import settings
from member.models import Person
# from sharing.models import Feed
from .models import prodProduct
from basket.models import Basket
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from orders.models import Order

import json
import os
import stripe

# Create your views here.

def history(request):
    try:
        product=prodProduct.objects.all()
        person=Person.objects.get(Email=request.session['Email'])
        user=Person.objects.all()
        allBasket = Basket.objects.all().filter(Person_fk_id=person.id,is_checkout=1)
        context = {
            'allBasket': allBasket,
            'product': product,
            'person': person,
            'user': user,
        }
        return render(request,'history.html', context)
    except prodProduct.DoesNotExist:
        raise Http404('Data does not exist')

def invoice(request,fk1):
    ids = Basket.objects.get(id=fk1)
    basket = Basket.objects.all().filter(transaction_code=ids.transaction_code)
    order = Order.objects.get(transaction_code=ids.transaction_code)
    return render(request,'invoice.html',{'basket':basket,'order':order})  