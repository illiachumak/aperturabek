from django.db import models
from accounts import models as ac
from store import models as st
from django.contrib.postgres.fields import ArrayField
from store.models import Product, Color
# Create your models here.

class Order(models.Model):
    PENDING = 'ОЧІКУЄТЬСЯ'
    WORKING = 'В ОБРОБЦІ'
    DONE = 'ВИКОНАНО'
    ORDER_STATUS = [
        (PENDING, 'ОЧІКУЄТЬСЯ'),
        (WORKING, 'В ОБРОБЦІ'),
        (DONE, 'ВИКОНАНО'),
    ]

    name = models.CharField(max_length = 250)
    order_number = models.CharField(max_length = 100, blank=True)
    number = models.CharField(max_length = 200)
    email = models.EmailField(max_length = 250, null = True)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 50, choices = ORDER_STATUS, default = PENDING)
    payment = models.BooleanField(default = False)
    total_price = models.DecimalField(decimal_places = 2, max_digits = 10)


    def __str__(self) -> str:
        return self.email


class OrderProduct(models.Model):
    product_name = models.CharField(max_length = 200)
    color = models.CharField(max_length = 200, blank = True, null = True)
    image = models.CharField(max_length = 1000, default = None, blank = True)
    modifications = ArrayField(models.IntegerField(), blank = True ,null = True)
    price = models.FloatField(default = 0.0)
    quantity = models.IntegerField(default = 1)
    orderId = models.ForeignKey(Order, on_delete = models.CASCADE)
    
    def __str__(self) -> str:
        return self.product_name
    
class Feedback(models.Model):
    name = models.CharField(max_length = 200)
    number = models.CharField(max_length = 50)
    is_Called = models.BooleanField(default = False)

    def __str__(self) -> str:
        return self.name
