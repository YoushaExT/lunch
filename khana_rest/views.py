# Create your views here.
from khana_rest.serializers import FoodItemSerializer, OrderSerializer, ShopSerializer, DateSerializer, TempUserSerializer, UserSerializer
from django.shortcuts import render
from django.http import HttpResponse#, JsonResponse
# from rest_framework.parsers import JSONParser
from khana.models import FoodItem, Order, Date, Shop, TempUser
from django.contrib.auth.models import User
#from rest_framework.decorators import api_view
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
            return False
            # return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FoodItemSerializer(item)
        return Response(serializer.data)
    
    def put(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FoodItemSerializer(item, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderAPIView(APIView):

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetails(APIView):

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        
        except Order.DoesNotExist:
            return False
            #return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        order = self.get_object(pk)
        if not order:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def put(self, request, pk):
        order = self.get_object(pk)
        if not order:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = self.get_object(pk)
        if not order:
            return Response(status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShopAPIView(APIView):

    def get(self, request):
        shops = Shop.objects.all()
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ShopSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopDetails(APIView):

    def get_object(self, pk):
        try:
            return Shop.objects.get(pk=pk)
        
        except Shop.DoesNotExist:
            return False
            #return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        shop = self.get_object(pk)
        if not shop:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ShopSerializer(shop)
        return Response(serializer.data)
    
    def put(self, request, pk):
        shop = self.get_object(pk)
        if not shop:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ShopSerializer(shop, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        shop = self.get_object(pk)
        if not shop:
            return Response(status=status.HTTP_404_NOT_FOUND)
        shop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DateAPIView(APIView):

    def get(self, request):
        dates = Date.objects.all()
        serializer = DateSerializer(dates, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DateDetails(APIView):

    def get_object(self, pk):
        try:
            return Date.objects.get(pk=pk)
        
        except Date.DoesNotExist:
            return False
            #return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        date = self.get_object(pk)
        if not date:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DateSerializer(date)
        return Response(serializer.data)
    
    def put(self, request, pk):
        date = self.get_object(pk)
        if not date:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DateSerializer(date, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        date = self.get_object(pk)
        if not date:
            return Response(status=status.HTTP_404_NOT_FOUND)
        date.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPIView(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetails(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        
        except User.DoesNotExist:
            return False
            # return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TempUserAPIView(APIView):

    def get(self, request):
        tempusers = TempUser.objects.all()
        serializer = TempUserSerializer(tempusers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TempUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TempUserDetails(APIView):

    def get_object(self, pk):
        try:
            return TempUser.objects.get(pk=pk)
        
        except TempUser.DoesNotExist:
            return False
            # return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        tempuser = self.get_object(pk)
        if not tempuser:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TempUserSerializer(tempuser)
        return Response(serializer.data)
    
    def put(self, request, pk):
        tempuser = self.get_object(pk)
        if not tempuser:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TempUserSerializer(tempuser, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tempuser = self.get_object(pk)
        if not tempuser:
            return Response(status=status.HTTP_404_NOT_FOUND)
        tempuser.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def rest_api_documentation(request):
    if request.method == 'GET':
        return render(request, 'khana_rest/api_documentation.html')
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