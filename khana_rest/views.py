# Create your views here.
from khana_rest.serializers import FoodItemSerializer
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from khana.models import FoodItem
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


#from django.contrib.auth.decorators import login_required
# Create your views here.

class FoodItemAPIView(APIView):

    def get(self, request):
        food_items = FoodItem.objects.all()
        serializer = FoodItemSerializer(food_items, many=True)
        #return JsonResponse(serializer.data, safe=False)
        return Response(serializer.data)

    def post(self, request):
        serializer = FoodItemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FoodItemDetails(APIView):

    def get_object(self, pk):
        try:
            return FoodItem.objects.get(pk=pk)
        
        except FoodItem.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = FoodItemSerializer(item)
        return Response(serializer.data)
    
    def put(self, request, pk):
        item = self.get_object(pk)
        serializer = FoodItemSerializer(item, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# # List all food items
# #@login_required
# @api_view(['GET', 'POST'])
# def food_item_list(request):
#     if request.method == 'GET':
#         food_items = FoodItem.objects.all()
#         serializer = FoodItemSerializer(food_items, many=True)
#         #return JsonResponse(serializer.data, safe=False)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         #serializer = FoodItemSerializer(data=request.data)
#         pass
#         # todo