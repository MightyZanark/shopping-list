from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.urls import reverse
from django.core import serializers

from main.forms import ProductForm
from main.models import Product


def show_main(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    
    context = {
        'name': 'Juan Maxwell Tanaya',
        'class': 'PBP C',
        'products': products
    }

    return render(request, "main.html", context)


def create_product(request: HttpRequest) -> HttpResponseRedirect | HttpResponse:
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "create_product.html", context)


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
