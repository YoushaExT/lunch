from rest_framework import serializers
from khana.models import FoodItem, Order, Shop, Date, TempUser
from django.contrib.auth.models import User

class FoodItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FoodItem
        #fields = ['id', 'name', 'price', 'shop']
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = '__all__'

class DateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Date
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class TempUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TempUser
        fields = '__all__'