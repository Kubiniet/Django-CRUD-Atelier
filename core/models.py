from asyncio import tasks
from turtle import title
from django.db import models
from django.shortcuts import reverse

SECTIONS_CHOICES = (
    ("BL", "BLUSAS"),
    ('SV', 'SAYAS /VESTIDOS'),
    ('RI', 'ROPA INTERIOR'),
    ('PL', 'Pantalones/Licras'),
    ('CP', 'CAMISAS/ PULOVERES '),
    ('PH', 'PANTALONES DE HOMBRE'),
    ('MI', 'MIXTOS')
)
RATE_ORDER_CHOICES = (
    ("1", 'nunca mas'),
    ('2', 'mas menos'),
    ('3', 'lo normal'),
    ('4', 'todo lindo,todo ok')
)

# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=30)
    adress = models.CharField(max_length=30, verbose_name='La puta direccion')
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=10, null=True)
    phone2 = models.CharField(max_length=10, blank=True, null=True)
   

    def __str__(self):
        return self.name

    def get_absolute_url(self):

        return reverse('core:detail_client', kwargs={'pk': self.pk})

    

    def get_delete_client_url(self):
        return reverse("core:del_client", kwargs={
            'pk': self.pk})


class Service(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    section = models.CharField(choices=SECTIONS_CHOICES, max_length=2)

    def __str__(self):
        section = self.get_section_display()
        return str(f' {section} {self.name} ')
    

    def get_absolute_url(self):
        return reverse('core:detail_service', kwargs={'pk': self.pk})

    def get_add_to_cart_url(self):
        return reverse('core:add-to-cart', kwargs={'pk': self.pk})

    def get_remove_from_cart_url(self):
        return reverse('core:remove-from-cart', kwargs={'pk': self.pk})

class OrderService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    ordered = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.service.name} x {self.quantity} "
    
    def get_total_price(self):
        return self.quantity * self.service.price

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateField()
    service = models.ManyToManyField(OrderService)
    ordered = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    extra_price = models.FloatField(default=0)
   
    def get_final_price(self):
        total=0
        for order_item in self.service.all():
            total += order_item.get_total_price()
            if self.extra_price:
                total += self.extra_price
        return total

    def get_delivery_time(self):
        time = self.start_date.date()
        days = self.order_date
        res = days - time

        return res.days

    class Meta():
        ordering = ['-start_date']

class Task(models.Model):
    title= models.CharField(max_length=200)
    task = models.TextField(max_length=400)
    stamptime=models.DateTimeField(auto_now_add=True)
    done=models.BooleanField(default=False)

    class Meta():
        ordering =['-stamptime']