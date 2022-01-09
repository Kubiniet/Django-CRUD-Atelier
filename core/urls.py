from django.urls import path
from .views import (ClientView, DetailClient,
                    DelClient, OrderView, ServiceView, DetailOrder)
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [
    path('panel/clientes/', ClientView.as_view(), name='clientes'),
    path('panel/clientes/<pk>/', DetailClient, name="detail_client"),
    path('delete_client/<pk>/', DelClient, name="del_client"),
    path('panel/servicios/', ServiceView.as_view(), name='services'),
    path('pedidos/', OrderView.as_view(), name='orders'),
    path('detail_order/<int:pk>/', DetailOrder, name="detail_order")
]
