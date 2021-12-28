from django.contrib import admin

# Register your models here.
from AtelierWebApp.models import Cliente,Servicio,Pedido

class ClienteAdmin(admin.ModelAdmin):
    list_display=('name','adress','phone','email')
    search_fields=('name','phone')

class ServicioAdmin(admin.ModelAdmin):
    list_filter=('name','genre','seccion','price')
    
class PedidoAdmin(admin.ModelAdmin):
    list_display=('fecha','numero','cliente','servicio')
    list_filter=('fecha','numero')
    date_hierarchy='fecha'

admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Servicio,ServicioAdmin)
admin.site.register(Pedido,PedidoAdmin)