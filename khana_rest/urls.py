from django.urls import path
# from django.urls.resolvers import URLPattern
from .views import FoodItemAPIView, FoodItemDetails, OrderAPIView, OrderDetails, DateAPIView, DateDetails, ShopAPIView, ShopDetails, UserAPIView, UserDetails, TempUserAPIView, TempUserDetails, rest_api_documentation, DateToday #, food_item_list

urlpatterns = [
    #path('food_items/', food_item_list),
    path('', rest_api_documentation),
    path('food_items/', FoodItemAPIView.as_view()),
    path('food_items/<int:pk>/', FoodItemDetails.as_view()),
    path('orders/', OrderAPIView.as_view()),
    path('orders/<int:pk>', OrderDetails.as_view()),
    path('dates/', DateAPIView.as_view()),
    path('dates/<int:pk>', DateDetails.as_view()),
    path('shops/', ShopAPIView.as_view()),
    path('shops/<int:pk>', ShopDetails.as_view()),
    path('users/', UserAPIView.as_view()),
    path('users/<int:pk>', UserDetails.as_view()),
    path('temp_users/', TempUserAPIView.as_view()),
    path('temp_users/<int:pk>', TempUserDetails.as_view()),
    path('date_today/', DateToday.as_view()),
]