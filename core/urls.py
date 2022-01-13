from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (ClientView, DetailClient,
                    DelClient, HomeView, OrderView, ServiceView, DetailOrder, MonthOrderView, SetPaid, SetPaidByDate, CustomLoginView, get_data, UpdateService, DelService)
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [
    path('panel/clientes/', ClientView.as_view(), name='clientes'),
    path('panel/clientes/<pk>/', DetailClient, name="detail_client"),
    path('delete_client/<pk>/', DelClient, name="del_client"),
    path('panel/servicios/', ServiceView.as_view(), name='services'),
    path('panel/pedidos/', OrderView.as_view(), name='orders'),
    path('detail_order/<int:pk>/', DetailOrder, name="detail_order"),
    path('pedidos/<int:year>/<int:month>/',
         MonthOrderView.as_view(month_format='%m'),
         name="archive_month_numeric"),
    path("pedidos/<int:pk>/ispaid/", SetPaid,
         name='ispaid'),
    path("pedidos/<int:pk>/<int:year>/<int:month>/ispaidbydate/", SetPaidByDate,
         name='ispaidbydate'),
    path('', HomeView.as_view(), name="home"),
    path('api/data/', get_data, name="feo"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='core:login'), name='logout'),
    path('detail_service/<int:pk>/', UpdateService, name='detail_service'),
    path('delete_serv/<pk>/', DelService, name='del_serv')
]
