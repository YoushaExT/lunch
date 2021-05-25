from rest_framework import serializers
from khana.models import FoodItem, Order, Shop, Date, TempUser

class FoodItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'price', 'shop']