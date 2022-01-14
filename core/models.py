from django.db import models
from django.db.models.fields import related
from django.shortcuts import reverse
import datetime

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
    description = models.TextField(max_length=200, blank=True, null=True)
    isbad = models.BooleanField(
        default=False, verbose_name="Esta en la lista negra")

    def __str__(self):
        return self.name

    def get_absolute_url(self):

        return reverse('core:detail_client', kwargs={'pk': self.pk})

    def get_add_to_cart_url(self):
        return reverse('core:add-to-cart', kwargs={'slug': self.slug})

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


class Order(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='order')
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    extra_price = models.FloatField(default=0)
    reasons = models.TextField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.service.price + self.extra_price

    def get_absolute_url(self):
        return reverse('core:detail_order', kwargs={'pk': self.pk})

    def get_delivery_time(self):
        time = self.start_date.date()
        days = self.order_date
        res = days - time

        return res.days

    class Meta():
        ordering = ['-start_date']