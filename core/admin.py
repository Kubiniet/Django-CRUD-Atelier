from django.contrib import admin
from .models import Client, Service,  Order, OrderService,Task
# Register your models here.


admin.site.register(Client)
admin.site.register(Service)

admin.site.register(Order)
admin.site.register(OrderService)
admin.site.register(Task)
