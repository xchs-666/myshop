from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .cart import Cart


def cart_detail(request):
    """购物车详情页"""
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


def cart_add(request, product_id):
    """加入购物车"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product, quantity=1)
    messages.success(request, f'「{product.name}」已加入购物车')
    return redirect('cart:detail')


def cart_remove(request, product_id):
    """从购物车移除"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'「{product.name}」已从购物车移除')
    return redirect('cart:detail')


def cart_update(request, product_id):
    """更新购物车商品数量"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart.add(product, quantity=quantity, update=True)
    else:
        cart.remove(product)
    return redirect('cart:detail')
