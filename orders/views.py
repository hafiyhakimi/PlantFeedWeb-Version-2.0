from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from marketplace.models import prodProduct
from django.core.cache import cache
from basket.models import Basket
from .models import Person
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

def cancel_order(request):
    transaction_code = request.POST.get('transaction_code')

    order_obj = Order.objects.get(transaction_code=transaction_code)
    order_obj.status = "Cancel"
    order_obj.save()
    
    basket_obj = Basket.objects.filter(transaction_code=transaction_code)
    basket_obj.update(status="Cancel")

    return JsonResponse({'status': 1, 'message': 'status updated to Cancelled'})

def complete_order(request):
    transaction_code = request.POST.get('transaction_code')

    order_obj = Order.objects.get(transaction_code=transaction_code)
    order_obj.status = "Order Received"
    order_obj.save()
    
    basket_obj = Basket.objects.filter(transaction_code=transaction_code)
    basket_obj.update(status="Order Received")

    return JsonResponse({'status': 1, 'message': 'status updated to Completed'})


def invoice(request,fk1):
    ids = Basket.objects.get(id=fk1)
    basket = Basket.objects.all().filter(transaction_code=ids.transaction_code)
    order = Order.objects.get(transaction_code=ids.transaction_code)
    return render(request,'invoice.html',{'basket':basket,'order':order})

def order_again(request, transaction_code):
    basket = Basket.objects.filter(transaction_code=transaction_code, is_checkout=1)
    for item in basket:
        product = item.productid
        user = item.Person_fk
        productqty = item.productqty

    if product.productStock < productqty:
        messages.error(request, f'{product.productName}(s) exceeds the stock limit in your basket')
        return redirect('../../../MainMarketplace.html')

    basket = Basket.objects.filter(productid=product, Person_fk=user, is_checkout=0)

    if len(basket) > 0:
        basket = Basket.objects.get(Person_fk=user, productid=product, is_checkout=0)
        if basket.productqty + productqty > product.productStock:
            messages.error(request, f'{product.productName}(s) exceeds the stock limit in your basket')
            return redirect('../../../MainMarketplace.html')
        basket.productqty += productqty
        basket.save()

        messages.success(request, 'Previous order successfully added to your basket')
        return redirect('basket:summary',)
    else:
        basket = Basket(productqty=productqty, productid=product, Person_fk=user, is_checkout=0,
                        transaction_code='').save()

    return redirect('basket:summary',)

#SELLER's HISTORY
def SellHistory(request, fk1):
    seller = Person.objects.get(pk=fk1)
    products = prodProduct.objects.all().filter(Person_fk=seller)
    product_ids = [product.productid for product in products]
    baskets = Basket.objects.all().filter(productid__in=product_ids, is_checkout=1)
    transactions = [basket.transaction_code for basket in baskets]
    orders = Order.objects.all().filter(transaction_code__in=transactions)
    products_by_order = {}
    unique_transactions = set()
    for order in orders:
        if order.transaction_code in unique_transactions:
            continue
        unique_transactions.add(order.transaction_code)
        product_baskets = Basket.objects.all().filter(transaction_code__in=[o.transaction_code for o in orders.filter(transaction_code=order.transaction_code)])
        products = []
        for product_basket in product_baskets:
            products.append({
                "address": order.address,
                "total": order.total,
                "shipping": order.shipping,
                "productQty": product_basket.productqty,
                "productName": product_basket.productid.productName,
                "productDesc": product_basket.productid.productDesc,
                "productPrice": product_basket.productid.productPrice,
                "productCategory": product_basket.productid.productCategory,
                "orderStatus": order.status,
            })
        products_by_order[order.transaction_code] = {
            "transaction_code": product_basket.transaction_code,
            "buyer_email": order.email,
            "buyer_name": order.name,
            "products": products,
            "orderStatus": order.status
        }
    if len(products_by_order) > 0:
        return render(request, 'SellHistory.html', {'products_by_order': products_by_order})
    else:
        return render(request, 'SellHistory.html', {'message': 'No orders found. Start selling your items!'})

def update_order_status(request):
    order_id = request.POST.get('order_id')
    order_status = request.POST.get('order_status')
    
    order_obj = Order.objects.get(transaction_code=order_id)
    order_obj.status = order_status
    order_obj.save()

    basket_objs = Basket.objects.filter(transaction_code=order_id)
    for basket_obj in basket_objs:
        basket_obj.status = order_status
        basket_obj.save()
    
    response = {'status': 1, 'message': 'Order status updated successfully'}
    
    return HttpResponse(json.dumps(response), content_type='application/json')