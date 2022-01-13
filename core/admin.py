from django.contrib import admin
from .models import Client, Service, Order
# Register your models here.


admin.site.register(Client)
admin.site.register(Service)

admin.site.register(Order)
