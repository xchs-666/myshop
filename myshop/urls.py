from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/login/', auth_views.LoginView.as_view(), name='login'),
    path('account/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('', include('products.urls')),
]

# 开发环境下提供媒体文件访问
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
