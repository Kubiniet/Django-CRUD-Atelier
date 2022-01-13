from django import forms
from .models import Client, Order, Service
from django.utils.dateparse import parse_datetime
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
import datetime

BIRTH_YEAR_CHOICES = ['2022', '2023', '2024']


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'
        labels = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[str(field)].label = ''

        self.fields['name'].widget.attrs.update(
            {"placeholder": 'Nombre del servicio'})
        self.fields['adress'].widget.attrs.update(
            {"placeholder": 'Direccion'})
        self.fields['email'].widget.attrs.update(
            {"placeholder": 'Correo'})
        self.fields['phone'].widget.attrs.update(
            {"placeholder": 'Telefono'})
        self.fields['phone2'].widget.attrs.update(
            {"placeholder": 'Telefono #2'})
        self.fields['description'].widget.attrs.update(
            {"placeholder": 'Descripcion del cliente'})
        self.fields['isbad'].label = 'La lista negra'


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = 'client', 'service', 'quantity', 'extra_price', "order_date", 'ordered', 'paid', 'reasons'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[str(field)].label = ''
            self.fields[str(field)].widget.attrs.update(
                {"placeholder": field})
        self.fields['order_date'].widget = forms.SelectDateWidget(
            years=BIRTH_YEAR_CHOICES, empty_label=("Año", "Mes", "Dia"), attrs={'style': 'display: inline-block; width: 33%;'})
        self.fields['paid'].label = 'Pagado'
        self.fields['ordered'].label = 'Entregado'
        self.fields['client'].empty_label = "Cliente"
        self.fields['service'].empty_label = "Servicio"


class NewOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('client', 'service', 'quantity', "order_date")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[str(field)].label = ''
            self.fields[str(field)].widget.attrs.update(
                {"placeholder": field})
        self.fields['order_date'].initial = datetime.date.today
        self.fields['order_date'].widget = forms.SelectDateWidget(
            years=BIRTH_YEAR_CHOICES, empty_label=("Año", "Mes", "Dia"), attrs={'style': 'display: inline-block; width: 33%;'})
        self.fields['client'].empty_label = "Cliente"
        self.fields['service'].empty_label = "Servicio"


class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[str(field)].label = ''

        self.fields['name'].widget.attrs.update(
            {"placeholder": 'Nombre de servicio'})
        self.fields['price'].widget.attrs.update(
            {"placeholder": 'Precio'})
