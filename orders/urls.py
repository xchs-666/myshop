from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='create'),
    path('<int:order_id>/', views.order_detail, name='detail'),
    path('<int:order_id>/pay/', views.order_pay, name='pay'),
    path('<int:order_id>/pay/process/', views.order_pay_process, name='pay_process'),
    path('', views.order_list, name='list'),
]
