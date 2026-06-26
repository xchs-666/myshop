from decimal import Decimal
from django.conf import settings
from products.models import Product


class Cart:
    """
    基于 Session 的购物车
    数据格式: { '1': {'quantity': 2, 'price': '39.90'}, '3': {...} }
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update=False):
        """添加商品到购物车"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
            }
        if update:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """从购物车移除商品"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """遍历购物车中的所有商品"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """购物车中商品种类数"""
        return len(self.cart)

    def get_total_price(self):
        """购物车总价"""
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def get_total_quantity(self):
        """购物车商品总数量"""
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        """清空购物车"""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True
