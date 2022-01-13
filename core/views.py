
from dataclasses import fields
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from .models import (Client, Service, Order)
from django.db.models import Sum, Avg, Max, Min, Count, F
from django.views.generic import CreateView, ListView, DetailView, View
from django.views.generic.dates import MonthArchiveView, timezone_today
from .forms import ClientForm, OrderForm, NewOrderForm, ServiceForm
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('core:home')


class ClientView(LoginRequiredMixin, ListView):
    template_name = "clients.html"
    model = Client

    def get_context_data(self, **kwargs):
        context = super(ClientView, self).get_context_data(**kwargs)
        context['form'] = ClientForm
        search_area = self.request.GET.get('search_area') or ''
        if search_area:
            context['object_list'] = context['object_list'].filter(
                name__icontains=search_area)
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


class ServiceView(LoginRequiredMixin, ListView):
    template_name = "services.html"
    model = Service
    ordering = ['section']

    def get_context_data(self, **kwargs):
        context = super(ServiceView, self).get_context_data(**kwargs)
        context['form'] = ServiceForm

        return context

    def post(self, request, *args, **kwargs):
        form = ServiceForm()
        try:
            if request.method == "POST":
                form = ServiceForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('core:services')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:services")


def UpdateService(request, pk):
    serv = get_object_or_404(Service, pk=pk)
    form = ServiceForm(request.POST or None, instance=serv)
    if form.is_valid():
        form.save()
        return redirect('core:services')
    return render(request, 'detail_service.html', {"serv": serv, 'form': form})


def DelService(request, pk):
    serv = Service.objects.get(pk=pk)
    serv.delete()
    return redirect('core:services')


class OrderView(LoginRequiredMixin, ListView):
    template_name = "new_order_form.html"
    model = Order
    ordering = ['paid', "-start_date"]

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['form'] = NewOrderForm()
        search_area = self.request.GET.get('search_area') or ''
        if search_area:
            context['object_list'] = context['object_list'].filter(
                client__name__icontains=search_area)
        return context

    def post(self, request, *args, **kwargs):
        form = NewOrderForm()
        try:
            print('intentando')
            if request.method == "POST":
                form = NewOrderForm(request.POST)
                if form.is_valid():
                    print('es valido')
                    form.save()
                    return redirect('core:orders')
                else:
                    return HttpResponse("no es valido")
        except ObjectDoesNotExist:
            print('no es valido')
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:orders")


def DetailOrder(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderForm(request.POST or None, instance=order)
    if form.is_valid():
        form.save()
        return redirect('core:orders')
    return render(request, 'detail_order.html', {"order": order, 'form': form})


class MonthOrderView(LoginRequiredMixin, MonthArchiveView):
    template_name = 'panel.html'
    queryset = Order.objects.all()
    date_field = 'order_date'
    allow_future = True
    ordering = ['paid', "-start_date"]

    def get_context_data(self, **kwargs):
        context = super(MonthOrderView, self).get_context_data(**kwargs)
        m = self.get_month()
        y = self.get_year()
        profit = Order.objects.filter(paid=True, order_date__month=m)
        profit_y = Order.objects.filter(paid=True, order_date__year=y)
        money = 0
        money_y = 0
        orders_months = self.object_list.count()
        for order in profit:
            money += order.quantity * order.service.price + order.extra_price
        for order in profit_y:
            money_y += order.quantity * order.service.price + order.extra_price
        context['feo'] = money
        context['money_y'] = money_y
        context['count'] = str(orders_months)
        context['count_m'] = str(profit.count())
        context['count_y'] = self.queryset.filter(
            order_date__year=y).count()
        return context


def get_profit_month(self):
    profit = self.objects.filter(paid=True)
    money = 0
    for order in profit:
        money += order.quantity * order.service.price
    return money


def SetPaid(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.paid = True
    order.save()
    # if
    return redirect("core:orders")


def SetPaidByDate(request, pk, year, month):
    order = get_object_or_404(Order, pk=pk)
    order.paid = True
    print(year)
    order.save()

    return redirect("core:archive_month_numeric", year, month)


class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profit = Order.objects.filter(paid=True)
        id = profit.values('client').annotate(
            Count('id')).order_by('-id__count').first()['client']

        best_client_orders = profit.filter(client_id=id)
        count_order_best_client = best_client_orders.count()
        cliente = best_client_orders[0].client.name
        count_client = Client.objects.count()
        service_id = profit.values('service').annotate(
            Count('id')).order_by('-id__count').first()['service']
        service_count = profit.filter(service_id=service_id).count()

        service = Service.objects.get(id=service_id).name

        money_client = best_client_orders.annotate(
            total=F("quantity") * F('service__price') + F('extra_price')).aggregate(Sum('total'))['total__sum']
        most_expensive_order = profit.annotate(
            total=F("quantity") * F('service__price') + F('extra_price')).aggregate(Max('total'))
        avg = profit.annotate(
            total=F("quantity") * F('service__price') + F('extra_price')).aggregate(Avg('total'))['total__avg']
        total = profit.annotate(
            total=F("quantity") * F('service__price') + F('extra_price')).aggregate(Sum('total'))['total__sum']
        context = {
            'total': total,
            'count': profit.count(),
            'client': cliente,
            'money_client': money_client,
            'count_orders_best_client': count_order_best_client,
            'count_client': count_client,
            'avg': avg,
            'most_expensive_order': most_expensive_order,
            'service': service,
            "count_service": service_count
        }
        return render(request, 'home.html', context)


def get_data(request, *args, **kwargs):

    labels = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
              'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    months = []
    orders = []
    amount = 0
    X = timezone_today()

    for i in range(13):
        amount = 0

        items = Order.objects.filter(
            paid=True, order_date__month=i).filter(order_date__lt=X + timedelta(days=31))

        for item in items:
            amount += (item.get_total_price())
        if items.exists():
            orders.append(amount)
            months.append(i)

    data = {
        "labels": labels[:len(months)],

        "default": orders,

    }
    return JsonResponse(data)
