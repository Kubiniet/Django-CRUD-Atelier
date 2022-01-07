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
            years=BIRTH_YEAR_CHOICES)


def handle_timezone(value, is_dst=None):
    if settings.USE_TZ and timezone.is_naive(value):
        return timezone.make_aware(value, timezone.get_current_timezone(), is_dst)
    elif not settings.USE_TZ and timezone.is_aware(value):
        return timezone.make_naive(value, timezone.utc)
    return value


class IsoDateTimeField(forms.DateTimeField):

    ISO_8601 = 'iso-8601'
    input_formats = [ISO_8601]

    def strptime(self, value, format):
        value = force_str(value)

        if format == self.ISO_8601:
            parsed = parse_datetime(value)
            if parsed is None:  # Continue with other formats if doesn't match
                raise ValueError
            return handle_timezone(parsed)
        return super().strptime(value, format)
