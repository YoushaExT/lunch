from django.urls import path
# from django.urls.resolvers import URLPattern
from .views import FoodItemAPIView, FoodItemDetails #, food_item_list

urlpatterns = [
    #path('food_items/', food_item_list),
    path('food_items/', FoodItemAPIView.as_view()),
    path('food_items/<int:pk>/', FoodItemDetails.as_view()),

]