from django.contrib.auth.models import User
from django.db import models
from django.contrib.sites.models import Site


#هون هعمل امبورت لمكتبة حمل منها الصور  pip install Pillow

    #هون علاقة انو عناصر المنيو بتنتمي لاكتر من كاتلوج يعني في عندي ساندويسات مليون سادويش وهكذا
class MenuItem(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField()
    image = models.ImageField(upload_to='static/images/', blank=True)
    price = models.IntegerField()
    category = models.ManyToManyField('Category', related_name='item')

    def __str__(self):#وهون انا ضفتها ليرجعلي اسم الاوبجكت يلي هكونو منها
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): #وهون انا ضفتها ليرجعلي اسم الاوبجكت يلي هكونو منها
        return self.name




    #هون انو الطلب تاعي يكون مكون من الايتم وسعرو طبعا ومتى تم الطلب
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.product.name) #هون ليظهرلي  اسماء الطلبات في صفحة الادمن




class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.address)


class OrderItem(models.Model):
    product = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=250)
    number_of_persons = models.IntegerField(default=0, null=True, blank=True)
    #number_of_tables = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    comment=models.TextField()
    buy=models.BooleanField()
    def __str__(self):

        return str(self.user)

        #rzp_test_BCHP97N8HlMg3J
        #DT7bQSKqlJpo3eVsDKMeXaZ4 هادا سيكرت كي