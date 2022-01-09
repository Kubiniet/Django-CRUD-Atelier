from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import (Client, Section, Service, Order)
from django.views.generic import CreateView, ListView, DetailView, View
from .forms import ClientForm, OrderForm, NewOrderForm
# Create your views here.


class ClientView(ListView):
    template_name = "clients.html"
    model = Client

    def get_context_data(self, **kwargs):
        context = super(ClientView, self).get_context_data(**kwargs)
        context['form'] = ClientForm
        return context

    def post(self, request, *args, **kwargs):
        form = ClientForm()
        try:
            if request.method == "POST":
                form = ClientForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('core:clientes')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:clientes")


def DetailClient(request, pk):
    client = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, instance=client)
    if form.is_valid():
        form.save()
        return redirect('core:clientes')
    return render(request, 'detail_client.html', {"client": client, 'form': form})


def DelClient(request, pk):
    client = Client.objects.get(pk=pk)
    client.delete()
    return redirect('core:clientes')


class ServiceView(ListView):
    template_name = "services.html"
    model = Service


class OrderView(ListView):
    template_name = "new_order_form.html"
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['form'] = NewOrderForm
        return context

    def post(self, request, *args, **kwargs):
        form = OrderForm()
        try:
            if request.method == "POST":
                form = OrderForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('core:orders')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:orders")


def DetailOrder(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderForm(request.POST or None, instance=order)
    if form.is_valid():
        form.save()
        return redirect('core:orders')
    return render(request, 'detail_order.html', {"order": order, 'form': form})
