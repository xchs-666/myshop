from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.cart import Cart
from .models import Order, OrderItem


@login_required
def order_create(request):
    """创建订单 — 填写收货信息"""
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, '购物车是空的，请先添加商品')
        return redirect('products:list')

    if request.method == 'POST':
        # 创建订单
        order = Order.objects.create(
            user=request.user,
            name=request.POST.get('name', ''),
            address=request.POST.get('address', ''),
            phone=request.POST.get('phone', ''),
        )
        # 创建订单项
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'],
            )
        # 清空购物车
        cart.clear()
        messages.success(request, '下单成功！感谢您的购买！')
        return redirect('orders:detail', order_id=order.id)

    return render(request, 'orders/create.html', {'cart': cart})


@login_required
def order_detail(request, order_id):
    """订单详情（确认页）"""
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})


@login_required
def order_list(request):
    """我的订单列表"""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/list.html', {'orders': orders})
