from django.db import models
from django.contrib.auth.models import User
# import datetime
# import pytz


# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class FoodItem(models.Model):
    name = models.CharField(max_length=64)
    price = models.IntegerField()
    # shop = models.CharField(max_length=64)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shops")

    def __str__(self):
        return f'{self.id} {self.name} {self.price} {self.shop}'


class Date(models.Model):
    date = models.DateField()

    def __str__(self):
        return f'{self.date}'


class Order(models.Model):
    quantity = models.IntegerField()
    date_id = models.ForeignKey(Date, on_delete=models.CASCADE, related_name="dates")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    item_id = models.ForeignKey(FoodItem, on_delete=models.DO_NOTHING, related_name="foods")

    def __str__(self):
        return f'{self.date_id} {self.item_id.name} {self.item_id.shop} {self.user_id} {self.item_id.price}$ {self.quantity}'


class TempUser(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    # created = models.DateTimeField(default=datetime.datetime.now(pytz.timezone('Asia/Karachi')))

    def __str__(self):
        return f'{self.username} - {self.created}'


# class Test(models.Model):
#     name = models.CharField(max_length=4)
