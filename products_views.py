from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from product.models import Product

@login_required(login_url="/")
def product_list(request):
    product_list = Product.objects.all()
    product_list = list(product_list)

    context = {
        "msg": "Hello world",
        "items": product_list
    }

    return render(request, "product/product_list.html", context)


def product_detail(request, prod_id):
    det = Product.objects.get(id=prod_id)

    context = {
        "details": det
    }
    return render(request, "product/details.html", context)


def get_create_product_page(request):
    return render(request, "product/product_create.html")


def create_product(request):
    prod_id = request.POST["id"]
    name = request.POST["name"]
    type = request.POST["type"]
    price = request.POST["price"]

    id_exists = Product.objects.filter(id=prod_id).exists()

    if id_exists:
        return HttpResponse("Id already exists")

    Product.objects.create(id=prod_id, name=name, type=type, price=price)

    return redirect("product:product_list")


def product_update(request, prod_id):
    prod = Product.objects.get(id=prod_id)

    context= {
        "product": prod
    }

    return render(request,"product/product_Update.html",context)