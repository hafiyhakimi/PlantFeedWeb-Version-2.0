from decimal import Decimal
from django.conf import settings
from django.db import models
from member.models import Person

from marketplace.models import prodProduct


class Order(models.Model):
    class Meta:
        db_table = 'Order'
    name = models.CharField(max_length=150, default="")
    email = models.CharField(max_length=1000, default="")
    address = models.CharField(max_length=1000, default="")
    payment = models.CharField(max_length=1000, default="")
    namecard = models.CharField(max_length=1000, default="")
    creditnumber = models.CharField(max_length=1000, default="")
    expiration = models.CharField(max_length=1000, default="")
    cvv = models.CharField(max_length=1000, default="")
    shipping = models.CharField(max_length=1000,null=True)
 
    transaction_code = models.CharField(max_length=1000, default="")
    total = models.FloatField(null=True)
    user = models.ForeignKey(Person, on_delete=models.CASCADE)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(prodProduct,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)