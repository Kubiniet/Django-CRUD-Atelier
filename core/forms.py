from django import forms
from .models import Client, Order
from django.utils.dateparse import parse_datetime
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone

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
            self.fields[str(field)].widget.attrs.update(
                {"placeholder": field})


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[str(field)].label = ''
            self.fields[str(field)].widget.attrs.update(
                {"placeholder": field})
        self.fields['order_date'].widget = forms.SelectDateWidget(
            years=BIRTH_YEAR_CHOICES, empty_label=("Dia", "Mes", "Año"),)
        self.fields['paid'].label = 'Pagado'
        self.fields['ordered'].label = 'Entregado'


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
        self.fields['order_date'].widget = forms.SelectDateWidget(
            years=BIRTH_YEAR_CHOICES, empty_label=("Año", "Mes", "Dia"))
