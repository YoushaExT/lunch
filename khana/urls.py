from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),

    path('<int:date_id>', views.index, name='table'),
    path('add', views.add, name='add'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('delete', views.delete_order, name='delete'),
    path('delete_temp', views.delete_temp, name='delete_temp'),
    path('update', views.update_order, name='update'),
    path('approve', views.approve_user, name='approve'),
    path('shop_filter', views.shop_filter, name='shop_filter'),
    path('all_my_orders', views.all_my_orders, name='all_my_orders'),
    path('filtered_index', views.filtered_index, name='filtered_index'),
    path('todays_orders', views.todays_orders, name='todays_orders'),
    path('print_orders', views.print_orders, name='print_orders'),
    # path('mail', views.send_a_mail),
    path('<str:useless>', views.default),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)