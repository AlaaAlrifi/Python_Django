import json
# رح اعملي تثبيت لمكتبة الدفع في جانغو pip install django-payments
# بروح على اليو ار الز وبعمل تعريف path('payments/', include('payments.urls')),
# رح اروح اعمل مودل لالها
# بروح على الاعدادات وبعرف تطبيق 'payments'
from datetime import datetime
from decimal import Decimal
import body as body
from django.core.mail import send_mail
from django.http import JsonResponse, request
from django.template.response import TemplateResponse
from django.core.validators import validate_email
# فت المكتبتين يلي فوق خاص بدالة الدفع
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from Pharmacy.models import MenuItem, Category, Order, OrderItem, Booking, UserInfo

def index(req):
    return render(req, 'index.html')


def sys(req):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()
    count = UserInfo.objects.count()
    return render(req, 'sys.html', {'categories': categories, 'menu_items': menu_items,'count':count})


def home(req):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()
    return render(req, 'home.html', {'categories': categories, 'menu_items': menu_items})


# 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 هادا السيكرت الخاص بجوجل تسجيل الدخول
# 561382438485-heghh3oagugdcum6nbi335quv9uri2rl.apps.googleusercontent.com هادا الاي دي
def register(req):
    if req.method == 'POST':
        username = req.POST['username']
        email = req.POST['email']
        password = req.POST['password']
        repeat_user_password = req.POST['repeat_user_password']
        if password == repeat_user_password:
            if len(password) > 8:
                if User.objects.filter(username=username).exists():
                    messages.warning(req, 'UserName is already taken ^_^')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.warning(req, 'Email is already taken ^_^')
                    return redirect('register')

                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()

                    # روحي على السيتنج واعملي الاعدادات كومنت عشان تامني جيميليك ومتى بدك تعرضيه للدكتور بتشيلي الكومنت وبتشيلي التحقق بخطوتين من جيميلك علشان م يعطي ارور

                    #return render(req, 'home.html')
                    return redirect('login')

            else:
                messages.warning(req, 'Password must be at least 8 characters ^_^')
                return redirect('register')


        else:
            messages.warning(req, 'Passwords not matching ^_^')
            return redirect('register')
    else:
        return render(req, 'signup.html')

    '''send_mail('Registration', 'You have just registered for a special site for fast food (Saj Restaurant) Welcome Dear ^_^..', email, [email],
                                 fail_silently=False)'''  # هون ارسلت للايميل يلي قام بالتسجيل ارسلتلو مسج على جيميلو من جيمميلك ي الاء في لسيتنج موجود


def login(req):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()
    if req.method == 'POST':
        email = req.POST['email']
        password = req.POST['password']
        user = User.objects.filter(email=email).first()
        if User.objects.filter(email=email).exists():
            if user.check_password(password):
                auth.login(req, user)  # هون عملت تسجيل دخول للمستخم في حالة كان موجود بالنظام
                '''send_mail('Registration',
                          'Allaaaaaa ^_^..','ala525748@gmail.com', ['mihsaan411@gmail.com'],
                          fail_silently=False)'''
                return render(req, 'home.html', {'categories': categories, 'menu_items': menu_items})
            else:
                messages.warning(req, 'The password you entered is incorrect, please try again....')
                return render(req, 'login.html')

        elif not User.objects.filter(email=email).exists():
            messages.warning(req, 'The email you entered is wrong, please check it.... ')
            return render(req, 'login.html')

    return render(req, 'login.html')


# اعادة تعيين كلمة المرور
def passwordReset(req):
    if req.method == 'POST':
        email = req.POST.get('email')
        new_password = req.POST.get('new_password')
        confirm_password = req.POST.get('confirm_password')
        print(new_password, confirm_password)
        user = get_object_or_404(User, email=email)
        if User.objects.filter(email=email).exists():
            if new_password != confirm_password:
                messages.warning(req, 'Password and confirm password do not match....')
                return render(req, 'passwordreset.html')
            elif len(new_password) < 8:
                messages.warning(req, 'Password must be at least 8 characters ^_^')
                return render(req, 'passwordreset.html')

            else:
                user.set_password(new_password)
                user.repeat_user_password = confirm_password
                user.save()
                return render(req, 'done.html')

        else:
            messages.warning(req, 'The email you entered does not exist....')
            return render(req, 'passwordreset.html')

    return render(req, 'passwordreset.html')


def reserve(req):
    total_tables = Booking.objects.count()
    # طبعا هون جبت ارسلت الكاتيجوريز عشان لو ضغط على المنيو يطلعلو القائمة كلها
    booking_cancel = Booking.objects.filter(buy=False)
    for x in booking_cancel:
        if Booking.objects.filter(buy=False).exists():
            booking_cancel.delete()

    categories = Category.objects.all()
    date = req.POST.get('date')
    timetables = req.POST.get('timetables')
    number_of_persons = req.POST.get('number_of_persons')
    #number_of_tables = req.POST.get('number_of_tables')
    phone = req.POST.get('phone')
    comment = req.POST.get('comment')
    if req.method == 'POST':
        if total_tables < 30:
            booking_table = Booking.objects.create(user=req.user, phone=phone, number_of_persons=number_of_persons,
                                                    date=date, time=timetables,
                                                   comment=comment, buy=False) #number_of_tables=number_of_tables,
            booking_table.save()
            print(booking_table.buy)
            booking = Booking.objects.filter(id=booking_table.id)
            return render(req, 'reservation_confirmation.html', {'booking': booking})
            '''
            
             total_number_of_tables = 0
             max_number_of_tables = 2
            if int(number_of_tables) < max_number_of_tables:
                print(total_number_of_tables < max_number_of_tables, type(number_of_tables), total_number_of_tables)
                total_number_of_tables = total_number_of_tables + int(number_of_tables)
                booking_table = Booking.objects.create(user=req.user, phone=phone, number_of_persons=number_of_persons,
                                                       number_of_tables=number_of_tables, date=date, time=timetables,
                                                       comment=comment, buy=False)
                booking_table.save()
                print(booking_table.buy)
                booking = Booking.objects.filter(id=booking_table.id)
                return render(req, 'reservation_confirmation.html', {'booking': booking})
            else:
                messages.error(req, 'The number of tables you want to book must be two or one...!')
                pass'''
        else:
            messages.warning(req, 'Sorry, all tables in the restaurant have been reserved...!')
            pass

    return render(req, 'reserve.html', {'categories': categories})


def reservation_confirmation(req, id):
    booking = Booking.objects.filter(id=id)
    return render(req, 'pay_to_reserve.html', {'id': id})


def res_succ(request, id):
    body = json.loads(request.body)
    print('BODY:', body)
    booking = Booking.objects.filter(id=id).update(buy=True)
    booking_cancel = Booking.objects.filter(buy=False)
    for x in booking_cancel:
        if Booking.objects.filter(buy=False).exists():
            booking_cancel.delete()
    return render(request, 'home.html')


def myBooking(req):
    booking = Booking.objects.filter(buy=True).values()
    booking_cancel = Booking.objects.filter(buy=False)
    for x in booking_cancel:
        if Booking.objects.filter(buy=False).exists():
            booking_cancel.delete()
    user_booking=Booking.objects.filter(user=req.user)
    #return render(req, 'myBooking2.html', {'booking': booking})
    return render(req, 'myBooking2.html', {'user_booking': user_booking})

    '''for x in Booking.objects.get(user=req.user) :
        if x.buy == True:
            return render(req, 'myBooking2.html', {'booking': booking})
        else:
            return render(req, 'home.html')

    return render(req, 'myBooking2.html', {'booking': booking})'''


def logout(req):
    auth.logout(req)
    return render(req, 'index.html')


def menu(req):
    menu_items = MenuItem.objects.all()
    categories = Category.objects.all()
    if 'search' in req.GET:
        search = req.GET['search']
        menu_items = MenuItem.objects.filter(name=search)
        return render(req, 'search.html', {'menu_items': menu_items})
    return render(req, 'menu.html', {'categories': categories, 'menu_items': menu_items})


def menu_details(req, id):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.filter(id=id)
    return render(req, 'details.html', {'categories': categories, 'menu_items': menu_items})


def category_name(req, id):
    if 'search' in req.GET:
        search = req.GET['search']
        menu_items = MenuItem.objects.filter(name=search)
        print(search)
        print(menu_items)
        return render(req, 'search.html', {'menu_items': menu_items})

    categories = Category.objects.all()
    menu_items = MenuItem.objects.filter(category=id)
    return render(req, 'categories.html', {'categories': categories, 'menu_items': menu_items})


def add_cart(req, id):
    menu_items = MenuItem.objects.get(id=id)
    if req.method == 'POST':
        quantity = req.POST.get('quantity')
        order = Order.objects.create(user=req.user, product=menu_items, complete=True, quantity=quantity)
        order.save()
        order_item = OrderItem.objects.create(product=order.product)
        order_item.save()
        return render(req, 'add_to_cart.html', {'menu_items': menu_items})

    else:
        return render(req, 'add_to_cart.html', {'menu_items': menu_items})


# لاحصل على السعر الكلي
def get_Total(orders):
    try:
        total = 0
        for x in orders:
            total = total + (x.product.price * x.quantity)
    except:
        pass
    return total


def get_quantity():
    orders = Order.objects.all()
    try:
        quantity = 0
        for x in orders:
            quantity = quantity + (x.quantity)
    except:
        pass
    return quantity




def showCart(req):
    categories = Category.objects.all()
    orders = Order.objects.filter(user=req.user.id)
    menu_items = MenuItem.objects.all()
    total_items = orders.count()
    total = get_Total(orders)
    query = orders.order_by('-created_on')
    page = req.GET.get('page', 1)
    paginator = Paginator(query, 3)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    return render(req, 'cart.html',
                  {'categories': categories, 'orders': orders, 'menu_items': menu_items, 'total': total,
                   'total_items': total_items})


# حزف طلب من الطلبات الموجودة في الكارت
def remove_from_cart(req, id):
    order = get_object_or_404(Order, id=id)
    if Order.objects.filter(id=id).exists():
        order.delete()
        # OrderItem.objects.filter(product=order.product).delete()
        return redirect('showCart')
    else:
        messages.warning(req, 'The order you want to remove does not already exist ')
        return render(req, 'cart.html')


def edit_item(req, id):
    order = get_object_or_404(Order, id=id)
    if req.method=='POST' :
        quantity = req.POST.get('quantity')
        order.quantity = quantity
        order.save()
        return render(req, 'edit.html', {'order': order})

    else:
        return render(req, 'edit.html', {'order': order})




#مش مهمة احزفيها
def completePay(req):
    orders = Order.objects.filter(user=req.user)
    total_items = orders.count()
    total = get_Total(orders)
    print(total_items, total)
    print(req.user)



def buyNow(request, id):
    order = Order.objects.get(id=id)
    print(order.product.price)
    total = order.product.price * order.quantity
    return render(request, "completePay2.html", {'order': order, 'total': total})



def paymentComplete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    order = Order.objects.get(id=body['productId'])
    OrderItem.objects.create(product=order.product)
    remove_from_cart(request, order.id)
    return JsonResponse('Payment completed!', safe=False)

def enter_your_data(req,id):
    none_user = UserInfo.objects.filter(address=None)
    for x in none_user:
        if UserInfo.objects.filter(address=None).exists():
            none_user.delete()
    address = req.POST.get('address')
    city = req.POST.get('city')
    phone = req.POST.get('phone')
    state = req.POST.get('state')
    zipcode = req.POST.get('zipcode')
    print(address, city, phone)
    count=UserInfo.objects.count()
    user = UserInfo.objects.filter(user=req.user)
    print(count)
    userInfo = UserInfo.objects.create(user=req.user, address=address, city=city, state=state,
                                       zipcode=zipcode,
                                       phone=phone)
    userInfo.save()
    return render(req, 'location.html',{'id':id})




