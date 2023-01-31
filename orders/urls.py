from django.urls import path
#from django.conf.urls import url
from . import views

app_name = 'orders'

urlpatterns = [
    path('history.html', views.history, name='history'),
    path('invoice.html/<str:fk1>/', views.invoice, name='invoice'),
]