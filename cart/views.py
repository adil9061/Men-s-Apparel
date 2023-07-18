from django.db.models import Count
from django.shortcuts import render,redirect
from django.views import View
from . models import Product,Customer,Cart,OrderPlaced,Payment,Wishlist
from .forms import RegistrationForm,ProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
@login_required
def home(request):
    i = 0
    j = 0
    if request.user.is_authenticated:
        i =len(Cart.objects.filter(user=request.user))
        j =len(Wishlist.objects.filter(user=request.user))
    return render(request, 'cart/index.html',locals())

@login_required
def about(request):
    i = 0
    j = 0
    if request.user.is_authenticated:
        i =len(Cart.objects.filter(user=request.user))
        j =len(Wishlist.objects.filter(user=request.user))
    return render(request, 'cart/about.html',locals())

@login_required
def contact(request):
    i = 0
    j = 0
    if request.user.is_authenticated:
        i =len(Cart.objects.filter(user=request.user))
        j =len(Wishlist.objects.filter(user=request.user))
    return render(request, 'cart/contact.html',locals())

@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self,request,val):
        i = 0
        j = 0
        if request.user.is_authenticated:
            i =len(Cart.objects.filter(user=request.user))
            j =len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"cart/category.html",locals())

@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        i = 0
        j = 0
        if request.user.is_authenticated:
            i =len(Cart.objects.filter(user=request.user))
            j =len(Wishlist.objects.filter(user=request.user))
        return render(request,"cart/category.html",locals())

@method_decorator(login_required,name='dispatch')
class ProductsDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        i = 0
        j = 0
        if request.user.is_authenticated:
            i =len(Cart.objects.filter(user=request.user))
            j =len(Wishlist.objects.filter(user=request.user))
        return render(request,"cart/productsdetail.html",locals())
    
class RegistrationView(View):
    def get(self,request):
        form = RegistrationForm()
        i = 0
        j = 0
        if request.user.is_authenticated:
            i =len(Cart.objects.filter(user=request.user))
            j =len(Wishlist.objects.filter(user=request.user))
        return render(request, 'cart/registraion.html',locals())
    def post(self,request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Successful!!!")
        else:
            messages.warning(request,"Something Wrong!!!")
        return render(request, 'cart/registraion.html',locals())
    
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = ProfileForm()
        i = 0
        j = 0
        if request.user.is_authenticated:
            i =len(Cart.objects.filter(user=request.user))
            j =len(Wishlist.objects.filter(user=request.user))
        return render(request, 'cart/profile.html',locals())
    def post(self,request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']
            
            pov = Customer(user=user,name=name,mobile=mobile,city=city,state=state,pincode=pincode)
            pov.save()
            messages.success(request,"Profile Successfully Created")
        else:
            messages.warning(request,"Something Wrong") 
        return render(request, 'cart/profile.html',locals())
 
@login_required   
def address(request):
    ads = Customer.objects.filter(user=request.user)
    i = 0
    j = 0
    if request.user.is_authenticated:
        i =len(Cart.objects.filter(user=request.user))
        j =len(Wishlist.objects.filter(user=request.user))
    return render(request, 'cart/address.html',locals())

@method_decorator(login_required,name='dispatch')
class UpdateAddress(View):
    def get(self,request,pk):
        ads = Customer.objects.get(pk=pk)
        form = ProfileForm(instance=ads)
        i = 0
        j = 0
        if request.user.is_authenticated:
            i =len(Cart.objects.filter(user=request.user))
            j =len(Wishlist.objects.filter(user=request.user))
        return render(request,'cart/updateaddress.html',locals())
    def post(self,request,pk):
        form = ProfileForm(request.POST)
        if form.is_valid():
            ads = Customer.objects.get(pk=pk)
            ads.name = form.cleaned_data['name']
            ads.city = form.cleaned_data['city']
            ads.mobile = form.cleaned_data['mobile']
            ads.state = form.cleaned_data['state']
            ads.pincode = form.cleaned_data['pincode']
            ads.save()
            messages.success(request,"Profile Update Successfully")
        else:
            messages.warning(request,"Something Wrong")
        return redirect("address")
    
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    i = 0
    j = 0
    if request.user.is_authenticated:
        i =len(Cart.objects.filter(user=request.user))
        j =len(Wishlist.objects.filter(user=request.user))
    return render(request,'cart/addtocart.html',locals())

@login_required
def show_wishlist(request):
    user = request.user
    i = 0
    j = 0
    if request.user.is_authenticated:
        i =len(Cart.objects.filter(user=request.user))
        j =len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render(request,"cart/wishlist.html",locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self,request):
        i = 0
        j = 0
        if request.user.is_authenticated:
            i =len(Cart.objects.filter(user=request.user))
            j =len(Wishlist.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_item = Cart.objects.filter(user=user)
        fullamount = 0
        for p in cart_item:
            value = p.quantity * p.product.discounted_price
            fullamount = fullamount + value
        totalamount = fullamount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount":razoramount,"currency":"INR","receipt":"order_rcptid_11"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        # {'id': 'order_MC77sPK7zOrM9t', 'entity': 'order', 'amount': 333700, 'amount_paid': 0, 'amount_due': 333700, 'currency': 'INR', 'receipt': 'order_rcptid_11', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1688995484}
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
        return render(request, 'cart/checkout.html',locals())
    
@login_required   
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    
    user = request.user
    
    customer = Customer.objects.get(id=cust_id)
    
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect("/orders")

@login_required
def orders(request):
    i = 0
    j = 0
    if request.user.is_authenticated:
        i =len(Cart.objects.filter(user=request.user))
        j =len(Wishlist.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'cart/orders.html',locals())
    

def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data={
            'message':'Wishlist Added Successfully'
        }
        return JsonResponse(data)
    
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data={
            'message':'Wishlist Removed Successfully'
        }
        return JsonResponse(data)
    
@login_required   
def search(request):
    query = request.GET['search']
    i = 0
    j = 0
    if request.user.is_authenticated:
        i =len(Cart.objects.filter(user=request.user))
        j =len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request,"cart/search.html",locals())