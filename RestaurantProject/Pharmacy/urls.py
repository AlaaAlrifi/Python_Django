from django.urls import path
from . import views, admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('sys/', views.sys, name='sys'),
    #path('search/', views.search, name='search'),
    path('reserve/', views.reserve, name='reserve'),
    path('menu/', views.menu, name='menu'),
    path('menu_details/<int:id>/', views.menu_details, name='menu_details'),
    path('menu/<int:id>/', views.category_name, name='category_name'),
    path('passwordReset/', views.passwordReset, name='passwordReset'),
    path('logout/', views.logout, name='logout'),
    path('myBooking/', views.myBooking, name='myBooking'),
    path('add_cart/<int:id>/', views.add_cart, name='add_cart'),
    path('res_succ/<int:id>', views.res_succ, name='res_succ'),
    path('showCart/', views.showCart, name='showCart'),
    path('remove_from_cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    #path('checkout/', views.checkout, name='checkout'),
    path('completePay/', views.completePay, name='completePay'),
    #path('payments/', views.payments, name='payments'),
    path('edit_item/<int:id>/', views.edit_item, name='edit_item'),
    #path('edit_successful/', views.edit_successful, name='edit_successful'),
    path('complete/', views.paymentComplete, name="complete"),
    path('buyNow/<int:id>/', views.buyNow, name="buyNow"),
    #path('location/<int:id>/', views.location, name="location"),
    #path('location/', views.my_account, name="my_account"),
    #path('account/', views.account, name="account"),
    path('enter_your_data/<int:id>/', views.enter_your_data, name="enter_your_data"),
    #path('edit_user_info/', views.edit_user_info, name="edit_user_info"),
    path('reservation_confirmation/<int:id>/', views.reservation_confirmation, name="reservation_confirmation"),
    #path('payment_details/', views.payment_details, name='payment_details'),




]