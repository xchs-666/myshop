from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
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
        with transaction.atomic():
            # 检查库存
            for item in cart:
                product = item['product']
                if product.stock < item['quantity']:
                    messages.error(request, f'「{product.name}」库存不足，仅剩 {product.stock} 件')
                    return redirect('cart:detail')

            # 创建订单
            order = Order.objects.create(
                user=request.user,
                name=request.POST.get('name', ''),
                address=request.POST.get('address', ''),
                phone=request.POST.get('phone', ''),
            )

            # 创建订单项 + 扣库存
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
                # 扣库存
                product = item['product']
                product.stock -= item['quantity']
                product.save()

            # 清空购物车
            cart.clear()

        messages.success(request, '下单成功！请完成支付。')
        return redirect('orders:pay', order_id=order.id)

    return render(request, 'orders/create.html', {'cart': cart})


@login_required
def order_detail(request, order_id):
    """订单详情"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})


@login_required
def order_list(request):
    """我的订单列表"""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/list.html', {'orders': orders})


@login_required
def order_pay(request, order_id):
    """支付页面"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.paid:
        messages.info(request, '该订单已支付')
        return redirect('orders:detail', order_id=order.id)
    return render(request, 'orders/pay.html', {'order': order})


@login_required
def order_pay_process(request, order_id):
    """处理支付（模拟）"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.paid:
        messages.info(request, '该订单已支付')
        return redirect('orders:detail', order_id=order.id)

    if request.method == 'POST':
        # 模拟支付成功
        order.paid = True
        order.status = 'paid'
        order.save()
        messages.success(request, '支付成功！我们将尽快为您发货。')
        return redirect('orders:detail', order_id=order.id)

    return redirect('orders:pay', order_id=order.id)
