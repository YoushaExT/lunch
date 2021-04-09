from django.contrib import admin
from .models import FoodItem, Order, Date, Shop, TempUser
from django.contrib.auth.models import User, Group

# Register your models here.
admin.site.register(FoodItem)
admin.site.register(Order)
admin.site.register(Date)
# admin.site.register(User)
admin.site.register(Shop)
admin.site.register(TempUser)

# admin.site.register(Test)
# my version of admin
from django.contrib.admin import AdminSite

# from .models import FoodItem, Order, Date, Shop, TempUser

class MyAdminSite(AdminSite):
    site_header = 'Techwards Lunch Administration'
    # login_template =


admin_site = MyAdminSite(name='myadmin')

admin_site.login_template = 'khana/admin/login.html'

admin_site.register(User)
admin_site.register(Group)

admin_site.register(FoodItem)
admin_site.register(Order)
admin_site.register(Date)
admin_site.register(Shop)
admin_site.register(TempUser)

# admin_site.register(Test)