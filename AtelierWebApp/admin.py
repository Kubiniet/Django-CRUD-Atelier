from django.contrib import admin

# Register your models here.
from AtelierWebApp.models import Cliente,Servicio,Pedido,Genre,Seccion

class ClienteAdmin(admin.ModelAdmin):
    list_display=('name','adress','phone','email')
    search_fields=('name','phone')

class ServicioAdmin(admin.ModelAdmin):
    list_filter=('name','price','seccion')
    search_fields=('name','price')
    
class GenreAdmin(admin.ModelAdmin):
    list_filter=('name',)
    
class SeccionAdmin(admin.ModelAdmin):
    list_filter=('name',)
    
class PedidoAdmin(admin.ModelAdmin):
    list_display=('fecha','numero','cliente','servicio')
    list_filter=('fecha','numero')
    date_hierarchy='fecha'

admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Servicio,ServicioAdmin)
admin.site.register(Pedido,PedidoAdmin)
admin.site.register(Genre,GenreAdmin)
admin.site.register(Seccion,SeccionAdmin)