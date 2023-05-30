import json


from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.decorators.http import require_POST, require_GET

import product
from customers.models import Customers, Sales, Cust_Prod
from product.models import Product

def home_page(request):
    prod_list = list(Product.objects.all())
    context = {
        "products": prod_list,
    }
    return render(request,"customer/index.html",context)

@require_GET
def login_page(request):
    if request.user.is_authenticated:
        return redirect("customer:home_page")
    return render(request, "customer:home_page")


@require_POST
def login(request):
    username = request.POST["uname"]
    password = request.POST["psw"]

    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return redirect("product:product_list")
    else:
        return HttpResponse("please register")
        # context ={
        #     "msg":"please register",
        # }
        # return redirect("customer:home_page",context)

def logout(request):
    auth.logout(request)
    return redirect("customer:home_page")


@require_GET
def register(request):
    return render(request, "customer/register.html")

@require_POST
def verify_register(request, user=None):
    username = request.POST["uname"]
    if User.objects.filter(username=username).exists():
        return HttpResponse("username exists")
    f_name = request.POST["f_name"]
    l_name = request.POST["l_name"]
    address = request.POST["add"]
    email = request.POST["email"]
    phone = request.POST["phone"]
    password = request.POST["psw"]

    user =User.objects.create(username=username, first_name=f_name, last_name=l_name, email=email)
    user.set_password(password)
    user.save()
    Customers.objects.create(username=user, address=address, phone=phone )

    auth.login(request, user)
    return redirect("product:product_list")

@login_required(login_url="/")
@require_POST
def save_cart(request):
    items = request.POST["items"]
    # user_id = get_object_or_404(Customers,username=request.user)
    # user_order, status = Sales.objects.get_or_create(cus_id=user_id, is_ordered=False)
    # for item in items:
    #      price = Product.objects.filter(id=items['id'])
    #      tot_price = price.price*item['quan']
    #      order_item, status = Cust_Prod.objects.get_or_create(products=item['id'],quantity=item['quan'],price=tot_price)
    #      user_order.items.add(order_item)
    items = json.loads(items)
    request.session["cart"] = items

    return JsonResponse({"msg":"success"})

@require_GET
def load_cart(request):
    items = request.session.get("cart", [])
    return JsonResponse({"items": items})

# @require_GET
# def total_cart(request):
#     items = request.session.get("cart", [])
#     prod_list = Product.objects.all()
#     return JsonResponse({"items": items},{"prod":prod_list})

# def save_shoppingcart(request):
#     obj = request.POST["items"]
#     request.session['shop_cart'] = obj
#     return 1

@login_required(login_url="/")
@require_POST
def checkOut(request):
    items = request.session.get("cart", [])
    if len(items) > 0:
        user_id = get_object_or_404(User, username=request.user)
        user_order, status = Sales.objects.get_or_create(cus_id=user_id, is_ordered=False)
        print(status)
        sum = 0.0
        for item in items:
             prod = Product.objects.get(id=item['id'])
             print(item['id'])
             tot_price = (prod.price) *item['quant']
             sum+= tot_price
             order_item, status = Cust_Prod.objects.get_or_create(products=prod,quantity= item['quant'],price=tot_price)
             print(status)
             user_order.items.add(order_item)
        sum = sum + 150
        user_order.tot_cost = sum
        user_order.save()
        # messages.info(request, "items added to cart")
        if Sales.objects.filter(cus_id=user_id).exists():
            return JsonResponse({"msg":sum})
        else:
            return JsonResponse({"msg":"error"})
    else:
        return  JsonResponse({"msg":"No products selected"})


@login_required(login_url="/")
def remove_from_cart(request, item_id):
    item_to_delete = Cust_Prod.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('customer:shopping_cart'))


@login_required(login_url="/")
def shopping_cart(request):
    cart_list = list(request.session.get("cart", []))
    prod_list = list(Product.objects.all())
    context = {
        "products": prod_list,
        "cart_list": cart_list
    }
    return render(request, "customer/shopping_cart.html",context)

# @login_required(login_url="/")
# def load_shoppingCart(request):
#     cart_list = request.session.get("cart",[])
#     cart_list = json.loads(cart_list)
#     prod_list =Product.objects.all()
#     context = {
#         "products1":prod_list,
#         "cart_list": cart_list['id']
#     }
#     return render(request, "customer/shopping_cart.html", context)