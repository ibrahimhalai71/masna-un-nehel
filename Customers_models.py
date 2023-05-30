from django.db import models
from django.contrib.auth.models import User

from product.models import Product


class Customers(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=50, null=True)

class Cust_Prod(models.Model):
    # sal_id = models.ForeignKey(Sales, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity =models.IntegerField(default=1)
    # is_ordered = models.BooleanField(default=False)
    price=models.FloatField(default=1)

class Sales(models.Model):
    sal_id = models.AutoField(primary_key= True)
    cus_id = models.ForeignKey(User, on_delete=models.CASCADE)
    tot_cost=models.FloatField(null= True)
    delivery_cost=models.FloatField(default = 150)
    order_date = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(Cust_Prod)

# class Order(models.Model):
#     sal_id = models.AutoField(primary_key=True)
#     cus_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
#     is_ordered = models.BooleanField(default=False)
#     items = models.ManyToManyField(Cust_Prod)
#     date_ordered = models.DateTimeField(auto_now=True)
#
#     def get_cart_items(self):
#         return self.items.all()
#
#     def get_cart_total(self):
#         return sum([item.product.price for item in self.items.all()])
#
#     def __str__(self):
#         return '{0} - {1}'.format(self.owner, self.ref_code)

