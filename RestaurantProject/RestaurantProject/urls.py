from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Pharmacy.urls')),
    #path('paypal/', include('paypal.standard.ipn.urls')),
    #path('payments/', include('payments.urls')),#هون البايمنت اجت من المكتبة العرفتها في بايمنت
]