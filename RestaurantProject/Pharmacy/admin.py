from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User

from Pharmacy.models import MenuItem, Category, Order, Booking, OrderItem, UserInfo

# Register your models here.
admin.site.site_header="Admin Login"
site_title = " admin Portal"
index_title = "Welcome"
admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Booking)
admin.site.register(OrderItem)
admin.site.register(UserInfo)


'''py manage.py makemigrations
 
 طيب بدي احول هادا الكلام لجداول في الداتا تاعتي
 بحط هادا الامر في التيرمنال 
  py manage.py migrate'''