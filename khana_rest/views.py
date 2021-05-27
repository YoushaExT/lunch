# Create your views here.
from khana_rest.serializers import FoodItemSerializer
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from khana.models import FoodItem
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

# List all food items
@api_view(['GET', 'POST'])
def food_item_list(request):
    if request.method == 'GET':
        food_items = FoodItem.objects.all()
        serializer = FoodItemSerializer(food_items, many=True)
        #return JsonResponse(serializer.data, safe=False)
        return Response(serializer.data)

    elif request.method == 'POST':
        pass
        # todo