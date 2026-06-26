from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    """订单"""
    STATUS_CHOICES = [
        ('pending', '待付款'),
        ('paid', '已付款'),
        ('shipped', '已发货'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    name = models.CharField(max_length=100, verbose_name='收货人')
    address = models.CharField(max_length=250, verbose_name='收货地址')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='下单时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    paid = models.BooleanField(default=False, verbose_name='是否付款')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='订单状态')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '订单'
        verbose_name_plural = '订单'

    def __str__(self):
        return f'订单 #{self.id}'

    def get_total_cost(self):
        """计算订单总价"""
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """订单项"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='订单')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name='商品')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    quantity = models.PositiveIntegerField(default=1, verbose_name='数量')

    class Meta:
        verbose_name = '订单项'
        verbose_name_plural = '订单项'

    def __str__(self):
        return f'{self.product.name} × {self.quantity}'

    def get_cost(self):
        """小计"""
        return self.price * self.quantity
