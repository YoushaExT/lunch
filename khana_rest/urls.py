from django.urls import path
# from django.urls.resolvers import URLPattern
from .views import food_item_list

urlpatterns = [
    path('food_items/', food_item_list),
]