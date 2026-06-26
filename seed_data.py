import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from products.models import Product

products = [
    {"name": "iPhone 15 手机壳", "slug": "iphone-15-case", "description": "高品质硅胶材质，防摔防滑，精准开孔。支持 MagSafe 磁吸充电。", "price": 39.90, "stock": 200},
    {"name": "无线蓝牙耳机", "slug": "wireless-earbuds", "description": "续航 36 小时，主动降噪，IPX5 防水。佩戴舒适，音质出色。", "price": 199.00, "stock": 50},
    {"name": "机械键盘 RGB", "slug": "mechanical-keyboard-rgb", "description": "87 键紧凑布局，Cherry 红轴，全键 RGB 背光。", "price": 299.00, "stock": 30},
    {"name": "高数学习指南", "slug": "advanced-math-guide", "description": "通俗易懂的高等数学学习资料，适合考研复习和期末备考。", "price": 49.00, "stock": 100},
    {"name": "Type-C 数据线", "slug": "type-c-cable", "description": "100W 快充，USB 3.1 传输速度，编织线身耐磨耐用。", "price": 25.00, "stock": 500},
    {"name": "蓝牙音箱", "slug": "bluetooth-speaker", "description": "便携式蓝牙音箱，360° 环绕立体声，IP67 防水防尘。", "price": 159.00, "stock": 40},
]

for p in products:
    obj, created = Product.objects.get_or_create(slug=p["slug"], defaults=p)
    if created:
        print(f"Created: {obj.name}")
    else:
        print(f"Already exists: {obj.name}")

print("Done!")
