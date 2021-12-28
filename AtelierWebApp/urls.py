from django.urls import path
from AtelierWebApp import views

urlpatterns = [
    path('',views.home , name='home'),
    path('servicios',views.servicios , name='servicios'),
    path('tienda',views.tienda , name='tienda'),
    path('blogs',views.blogs , name='blogs'),
    path('contacto',views.contacto , name='contacto'),
    path('registrarCliente/',views.registrarCliente , name='registrarCliente '),
    path('editarCliente/<pk>',views.editarCliente , name='editarCliente'),
    path('conf_edit/',views.conf_edit , name='conf_edit'),
    path('eliminarCliente/<pk>',views.eliminarCliente , name='eliminarCliente'),
]
