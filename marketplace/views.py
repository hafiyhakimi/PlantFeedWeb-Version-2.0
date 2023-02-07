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
from member.models import Person
# from sharing.models import Feed
from .models import prodProduct
from basket.models import Basket
# from .models import Person

# Create your views here.


#marketplace
# def mainMarketplace(request):
#     try:
#         marketplace=MarketplaceFeed.objects.all()
#         return render(request,'MainMarketplace.html',{'marketplace':marketplace})
#     except MarketplaceFeed.DoesNotExist:
#         raise Http404('Data does not exist')
    
def mainMarketplace(request):
    try:
        marketplace=prodProduct.objects.all()
        # allBasket=Basket.objects.all()
        
        person = Person.objects.get(Email=request.session['Email'])
        
        allBasket = Basket.objects.filter(Person_fk_id=person.id,is_checkout=0)
        user=Person.objects.all()
        return render(request,'MainMarketplace.html',{'marketplace':marketplace, 'allBasket':allBasket, 'person':person, 'user':user})
    except prodProduct.DoesNotExist:
        raise Http404('Data does not exist')
    
def sellProduct(request, fk1):
    person = Person.objects.get(pk=fk1)
    if request.method=='POST':
        product = prodProduct()
        product.productName=request.POST.get('productName')
        product.productDesc=request.POST.get('productDesc')
        product.productPrice=request.POST.get('productPrice')
        product.productCategory=request.POST.get('productCategory')
        product.productStock=request.POST.get('productStock')
        
        if len(request.FILES) != 0:
            product.productPhoto=request.FILES['productPhoto']
        
        product.Person_fk=person
        
        product.save()

        messages.success(request,'Product Has Been Added Succesfully..!')

        return redirect('marketplace:MainMarketplace')
    else :
        return render(request,'SellProduct.html')
    
def deleteProduct(request,fk1):
    product = prodProduct.objects.get(pk=fk1)
    
    try:
        product = prodProduct.objects.get(pk=fk1)
        product.deleteProduct()
        return redirect('marketplace:MainMarketplace')
        
    except prodProduct.DoesNotExist:
        messages.success(request, 'The product does not exist')
        return redirect('marketplace:MainMarketplace')
    
def updateProduct(request,fk1):
    product = prodProduct.objects.get(pk=fk1) 
    if request.method == 'POST':
        product.productName=request.POST.get('productName')
        product.productDesc=request.POST.get('productDesc')
        product.productCategory=request.POST.get('productCategory')
        product.productPrice=request.POST.get('productPrice')
        
        if len(request.FILES) != 0:
            product.productPhoto=request.FILES['productPhoto']
            
        fss = FileSystemStorage()
        
        product.save()
        
        return redirect('marketplace:MainMarketplace')
    else:
        return render(request, 'UpdateProduct.html', {'product':product})
    
    def viewMarketplaceFeed(request):
        MarketplaceFeed = MarketplaceFeed.objects.all()
        person = Person.objects.filter(Email=request.session['Email'])
        return render(request,'ViewMarketplace.html',{'MarketplaceFeed':MarketplaceFeed, 'person':person})
    
def buy_now(request, fk1,fk2):
    product = prodProduct.objects.get(pk=fk1)
    user = Person.objects.get(pk=fk2)
    if request.method=='POST':
        productqty= int(request.POST.get('productqty'))
        basket = Basket.objects.filter(productid=product,Person_fk=user,is_checkout=0)

        if product.productStock < productqty:
            messages.error(request, f'{product.productName}(s) exceeds the stock limit in your basket')
            return redirect('../../../MainMarketplace.html')

        if len(basket) == 0 : 
            basket = Basket(productqty=productqty,productid=product,Person_fk=user,is_checkout=0,transaction_code='').save()
        else :
            basket = Basket.objects.get(Person_fk=user,productid=product,is_checkout=0)
            if basket.productqty + productqty > product.productStock:
                messages.error(request, f'{product.productName}(s) exceeds the stock limit in your basket')
                return redirect('../../../MainMarketplace.html')
            basket.productqty += productqty
            basket.save()
        
        messages.success(request,'Item successfully added to your basket')
        return redirect('basket:summary')
    return render(request, 'summary.html', {'basket': basket})


def add_to_basket(request, fk1,fk2):
    
    product = prodProduct.objects.get(pk=fk1)
    user = Person.objects.get(pk=fk2)
    if request.method=='POST':
        productqty= int(request.POST.get('productqty'))
        basket = Basket.objects.filter(productid=product,Person_fk=user,is_checkout=0)

        if product.productStock < productqty:
            messages.error(request, f'{product.productName}(s) exceeds the stock limit in your basket')
            return redirect('../../../MainMarketplace.html')

        if len(basket) == 0 : 
            basket = Basket(productqty=productqty,productid=product,Person_fk=user,is_checkout=0,transaction_code='').save()
        else :
            basket = Basket.objects.get(Person_fk=user,productid=product,is_checkout=0)
            if basket.productqty + productqty > product.productStock:
                messages.error(request, f'{product.productName}(s) exceeds the stock limit in your basket')
                return redirect('../../../MainMarketplace.html')
            basket.productqty += productqty
            basket.save()
        
        messages.success(request,'Item successfully added to your basket')
        return redirect('../../../MainMarketplace.html')
    return render(request, '../../../MainMarketplace.html', {'basket': basket})