from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from shop.models import Category, Product


@login_required
def product_list(request, category_slug=None):
    """вью списка товаров"""
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


@login_required
def product_detail(request, id, slug):
    """вью детальной информации о товаре"""
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    return render(request, 'shop/product/detail.html',
                  {'product': product})
