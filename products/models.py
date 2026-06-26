from django.db import models
from django.urls import reverse


class Product(models.Model):
    """商品模型"""
    name = models.CharField(max_length=200, verbose_name='商品名称')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL 别名')
    description = models.TextField(blank=True, verbose_name='商品描述')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    stock = models.PositiveIntegerField(default=0, verbose_name='库存')
    image = models.ImageField(upload_to='products/%Y/%m/', blank=True, verbose_name='商品图片')
    available = models.BooleanField(default=True, verbose_name='是否上架')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '商品'
        verbose_name_plural = '商品'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.slug])
