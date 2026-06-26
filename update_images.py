import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from products.models import Product

# 图片映射：数据库 slug → 图片文件名
mapping = {
    'iphone-15-case': '苹果15手机壳.png',
    'wireless-earbuds': '蓝牙耳机.png',
    'mechanical-keyboard-rgb': '机械键盘.png',
    'advanced-math-guide': '高等数学.png',
    'type-c-cable': 'type-c数据线.png',
    'bluetooth-speaker': '蓝牙音箱.png',
}

# 给已有商品绑定图片
for slug, filename in mapping.items():
    try:
        product = Product.objects.get(slug=slug)
        product.image = f'products/2026/06/{filename}'
        product.save()
        print(f'Updated: {product.name} → {filename}')
    except Product.DoesNotExist:
        print(f'Not found: {slug}')

# 新建日语N2语法书
new, created = Product.objects.get_or_create(
    slug='jlpt-n2-grammar',
    defaults={
        'name': '日语N2语法书',
        'description': '全面覆盖日语能力考试 N2 级别语法考点，包含 200+ 语法条目、详解例句、练习题库。适合备考日语 N2 的学习者使用。',
        'price': 59.00,
        'stock': 80,
        'image': 'products/2026/06/日语N2语法.png',
    }
)
if created:
    print(f'Created: {new.name}')
else:
    print(f'Already exists: {new.name}')
    new.image = 'products/2026/06/日语N2语法.png'
    new.save()

print('Done!')
