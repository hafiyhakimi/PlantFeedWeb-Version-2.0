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
from marketplace.models import prodProduct
from basket.models import Basket
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.utils import timezone
from orders.models import Order

import json
import os
import stripe
# from .models import Person

# Create your views here.
def pay(request):
    tcode = 'TRANS#'+str(timezone.now())
    person=Person.objects.get(Email=request.session['Email'])
    
    for bas in Basket.objects.all().filter(Person_fk_id=person.id,is_checkout=0) :
        prod = prodProduct.objects.all().get(productid=bas.productid.productid)
        prod.productStock -= bas.productqty
        if prod.productStock < 0 :
            return HttpResponse('Stock is not enough', content_type='application/json')
        else :
            prod.save()
    ord = Order()
    ord.name = request.POST['name']
    ord.email = request.POST['email']
    ord.address = request.POST['address']
    ord.payment = request.POST['payment']
    ord.creditnumber = request.POST['creditnumber']
    ord.expiration = request.POST['expiration']
    ord.cvv = request.POST['cvv']
    ord.transaction_code = tcode
    ord.user_id = person.id
    ord.namecard = request.POST['namecard']
    ord.shipping = request.POST['shipping']
    ord.total = request.POST['total']
    
    ord.save()
    Basket.objects.all().filter(Person_fk_id=person.id,is_checkout=0).update(is_checkout=1,transaction_code=tcode)
    return redirect('orders:history')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)
    
def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')


class Error(TemplateView):
    template_name = 'payment/error.html'