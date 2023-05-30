from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    picture = models.ImageField(default=None)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    type = models.CharField(max_length=100)
    weight = models.FloatField(default=150)


