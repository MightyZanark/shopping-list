import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.urls import reverse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from main.forms import ProductForm
from main.models import Product


@login_required(login_url='/login')
def show_main(request: HttpRequest) -> HttpResponse:
    products = Product.objects.filter(user=request.user)
    
    context = {
        'name': request.user.username,
        'class': 'PBP C',
        'products': products,
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "main.html", context)


def create_product(request: HttpRequest) -> HttpResponseRedirect | HttpResponse:
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "create_product.html", context)


def edit_product(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    product = Product.objects.get(pk=id)
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse("main:show_main"))
    
    context = {"form": form}
    return render(request, "edit_product.html", context)


def delete_product(request: HttpRequest, id: int) -> HttpResponseRedirect:
    product = Product.objects.get(pk=id)
    product.delete()
    return HttpResponseRedirect(reverse("main:show_main"))


def show_xml(request: HttpRequest) -> HttpResponse:
    data = Product.objects.all()
    return HttpResponse(
        serializers.serialize("xml", data), 
        content_type="application/xml"
    )


def show_json(request: HttpRequest) -> HttpResponse:
    data = Product.objects.all()
    return HttpResponse(
        serializers.serialize("json", data), 
        content_type="application/json"
    )


def show_xml_by_id(request: HttpRequest, id:int) -> HttpResponse:
    data = Product.objects.filter(pk=id)
    return HttpResponse(
        serializers.serialize("xml", data),
        content_type="application/xml"
    )


def show_json_by_id(request: HttpRequest, id: int) -> HttpResponse:
    data = Product.objects.filter(pk=id)
    return HttpResponse(
        serializers.serialize("json", data), 
        content_type="application/json"
    )


def register(request: HttpRequest) -> HttpResponse:
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been successfully created!")
            return redirect("main:login")
    
    context = {"form": form}
    return render(request, "register.html", context)


def login_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie("last_login", str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, "Sorry, incorrect username or password. Please try again.")
        
    context = {}
    return render(request, "login.html", context)


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    response = HttpResponseRedirect(reverse("main:login"))
    response.delete_cookie("last_login")
    return response
