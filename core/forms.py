from django import forms
from .models import Client, Order, OrderService,Service,Task
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import datetime

BIRTH_YEAR_CHOICES = ['2022', '2023', '2024']

class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[str(field)].label = ''
           
        self.fields['name'].widget.attrs.update(
            {"placeholder": 'Nombre completo'})
        self.fields['adress'].widget.attrs.update(
            {"placeholder": 'Dirección'})
        self.fields['email'].widget.attrs.update(
            {"placeholder": 'Correo'})
        self.fields['phone'].widget.attrs.update(
            {"placeholder": 'Teléfono'})
        self.fields['phone2'].widget.attrs.update(
            {"placeholder": 'Teléfono #2'})

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('client',  "order_date",'extra_price', 'service')
        
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
        self.fields['service'] = forms.ModelMultipleChoiceField(
        queryset=OrderService.objects.filter(ordered=False),
        widget=forms.CheckboxSelectMultiple(attrs={'style': 'margin:1px;'}), label="", initial=OrderService.objects.filter(ordered=False))
       
class UpdateOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('client',"order_date",'extra_price', 'service','ordered', 'paid')

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

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude = ('done',)     

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[str(field)].label = ''        
        self.fields['title'].widget.attrs.update(
            {"placeholder": 'Título'})
        self.fields['task'].widget.attrs.update(
            {"placeholder": 'Texto'})
        