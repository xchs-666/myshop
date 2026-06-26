from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Product


def product_list(request):
    """商品列表页"""
    products = Product.objects.filter(available=True)
    return render(request, 'products/list.html', {'products': products})


def product_detail(request, slug):
    """商品详情页"""
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'products/detail.html', {'product': product})


def register(request):
    """用户注册"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 注册后自动登录
            messages.success(request, '注册成功！欢迎加入！')
            return redirect('products:list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
