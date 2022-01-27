from django.urls import path
from .views import (ClientView, DetailClient,
                    DelClient,DelTask, OrderView,MonthOrderView,TodoListView,SetTaskDone, TaskUpdateView, ServiceView,CustomLoginView,OrderSummary,SetPaidByDate, SetPaid,add_to_cart,UpdateService,DelService,HomeView,get_data,DetailOrder,DelOrder,remove_from_cart)
from django.contrib.auth.views import LogoutView


app_name = 'core'

urlpatterns = [
     path('panel/clientes/', ClientView.as_view(), name='clientes'),
     path('panel/clientes/<pk>/', DetailClient, name="detail_client"),
     path('del_client/<pk>/', DelClient, name="del_client"),
     path('panel/servicios/', ServiceView.as_view(), name='services'),
     path('panel/pedidos/', OrderView.as_view(), name='orders'),
     path('panel/pedidos/<pk>/', DetailOrder, name="detail-order"),
     path("panel/pedidos/<int:pk>/ispaid/", SetPaid,
          name='ispaid'),
     path('panel/nuevo_pedido/',OrderSummary.as_view(),name='summary'),
     path('add-to-cart/<int:pk>/', add_to_cart, name='add-to-cart'),
     path('remove_from_cart/<int:pk>/', remove_from_cart, name='remove-from-cart'),
     path('detail_service/<int:pk>/', UpdateService, name='detail_service'),
     path('delete_serv/<pk>/', DelService.as_view(), name='del-serv'),
     path('',HomeView.as_view(),name='home'),
     path('api/data/', get_data, name="feo"),
     path('del_order/<pk>/', DelOrder.as_view(), name='del-order'),
     path('panel/pedidos/<int:year>/<int:month>/',
          MonthOrderView.as_view(month_format='%m'),
          name="orders-month"),
     path("pedidos/<int:pk>/<int:year>/<int:month>/ispaidbydate/", SetPaidByDate,
          name='ispaidbydate'),
     path('login/', CustomLoginView.as_view(), name='login'),
     path('logout/', LogoutView.as_view(next_page='core:login'), name='logout'),
     path('panel/task/',TodoListView.as_view(),name='task'),
     path('panel/task/<pk>/',TaskUpdateView.as_view(),name='detail-task'),
     path("panel/task/<int:pk>/isdone/", SetTaskDone,
          name='isdone'),
     path('del_task/<pk>/', DelTask.as_view(), name='del-task'), 
]
