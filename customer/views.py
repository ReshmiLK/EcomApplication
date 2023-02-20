from django.shortcuts import render,redirect

from customer.forms import RegistrationForm,LoginForm,ReviewForm
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from store.models import Products,Carts,Orders,Offers
from django.utils.decorators import method_decorator
# Create your views here.

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

class SignUpView(View):

    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"signup.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signup")
        else:
            return render(request,"signup.html",{"form":form})


class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                return render(request,"login.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class IndexView(View):
    def get(self,request,*args,**kwargs):
        qs=Products.objects.all()
        return render(request,"index.html",{"products":qs})


@method_decorator(signin_required,name="dispatch")
class ProductDetailView(View):
        def get(self,request,*args,**kwargs):
            id=kwargs.get("id")
            qs=Products.objects.get(id=id)
            return render(request,"productdetail.html",{"product":qs})


@method_decorator(signin_required,name="dispatch")
class AddToCartView(View):
    def post(self,request,*args,**Kwargs):
        qty=request.POST.get("qty")
        user=request.user
        id=Kwargs.get("id")
        product=Products.objects.get(id=id)
        Carts.objects.create(product=product,user=user,qty=qty)
        return redirect("home")


@method_decorator(signin_required,name="dispatch")
class CartListView(View):

    def get(self,request,*args,**kwargs):
        qs=Carts.objects.filter(user=request.user,status="in-cart")
        return render(request,"cart-list.html",{"carts":qs})


@method_decorator(signin_required,name="dispatch")
class CartRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Carts.objects.filter(id=id).update(status="cancelled")
        return redirect("home")


@method_decorator(signin_required,name="dispatch")
class MakeOrderView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Carts.objects.get(id=id)
        return render(request,"checkout.html",{"cart":qs})
    def post(elf,request,*args,**kwargs):
        user=request.user
        address=request.POST.get("address")
        id=kwargs.get("id")
        cart=Carts.objects.get(id=id)
        product=cart.product
        Orders.objects.create(product=product,
        user=user,
        address=address)
        cart.status="order-placed"
        cart.save()
        return redirect("home")

@method_decorator(signin_required,name="dispatch")
class MyOrderesView(View):
    def get(self,request,*args,**kwargs):
        qs=Orders.objects.filter(user=request.user).exclude(status="cancelled")
        return render(request,"order-list.html",{"orders":qs})
        
@method_decorator(signin_required,name="dispatch")
class OrderCancelView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Orders.objects.filter(id=id).update(status="cancelled")
        return redirect("my-orders")

@method_decorator(signin_required,name="dispatch")
class DiscountProductView(View):

    def get(self,request,*args,**kwargs):
        qs=Offers.objects.all()
        return render(request,"offer-products.html",{"offers":qs})


@method_decorator(signin_required,name="dispatch")
class ReviewCreateView(View):

    def get(self,request,*args,**kwargs):
        form=ReviewForm()
        return render(request,"review-add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=ReviewForm(request.POST)
        id=kwargs.get("id")

        pro=Products.objects.get(id=id)
        if form.is_valid():
            form.instance.user=request.user
            form.instance.product=pro
            form.save()
            return redirect("home")
        else:
            return render(request,"review-add.html",{"form":form})


def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")
    