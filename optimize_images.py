import os
from PIL import Image

media_dir = os.path.join(os.path.dirname(__file__), 'media', 'products', '2026', '06')
os.makedirs(media_dir, exist_ok=True)

for filename in os.listdir(media_dir):
    if not filename.endswith('.png'):
        continue

    filepath = os.path.join(media_dir, filename)
    original_size = os.path.getsize(filepath)

    img = Image.open(filepath)

    # 转 RGB（JPEG 不支持透明通道）
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    # 宽高最大 800px
    max_size = 800
    ratio = min(max_size / img.width, max_size / img.height, 1.0)
    if ratio < 1:
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)

    # 存为 JPEG，质量 85
    jpg_name = filename.replace('.png', '.jpg')
    jpg_path = os.path.join(media_dir, jpg_name)
    img.save(jpg_path, 'JPEG', quality=85, optimize=True)

    new_size = os.path.getsize(jpg_path)
    saved = original_size - new_size
    print(f'{filename}: {original_size//1024}KB → {new_size//1024}KB (节省 {saved//1024}KB)')

    # 删掉原 PNG
    os.remove(filepath)
    print(f'  已删除原文件: {filename}')

print('\n开始更新数据库...')
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
import sys
sys.path.insert(0, os.path.dirname(__file__))
django.setup()
from products.models import Product

for product in Product.objects.all():
    if product.image and product.image.name.endswith('.png'):
        product.image.name = product.image.name.replace('.png', '.jpg')
        product.save()
        print(f'  更新: {product.name} → {product.image.name}')

print('完成！')
