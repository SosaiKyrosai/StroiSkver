from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_list(request, category_slug=None):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'category_slug': category_slug,  # Передаем category_slug в контекст
    }
    return render(request, 'product_list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    return render(request, 'product_detail.html', {'product': product})


def all_products_filter(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    categories = Category.objects.all()  # Получаем все категории товаров

    return render(request, 'all_products_filter.html', {'products': products, 'categories': categories})


def category_products_filter(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    categories = Category.objects.all()

    products = Product.objects.filter(category=category)
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    return render(request, 'category_products_filter.html', {'products': products, 'category': category, 'categories': categories})


def category_product_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'category_product_list.html', {'products': products, 'category': category, 'categories': categories})

