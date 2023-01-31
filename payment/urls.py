from django.urls import path
#from django.conf.urls import url
from . import views

app_name = 'payment'

urlpatterns = [
    path('orderplaced/', views.order_placed, name='order_placed'),
    path('error/', views.Error.as_view(), name='error'),
    path('webhook/', views.stripe_webhook),
    path('pay', views.pay, name='pay'),
]