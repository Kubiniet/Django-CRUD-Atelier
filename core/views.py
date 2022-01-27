
from re import template
from django.forms import models
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.urls import reverse_lazy
from .models import (Client, Service, OrderService, Order, Task)
from django.views.generic import CreateView, ListView, DetailView, View,TemplateView,DeleteView,UpdateView
from .forms import ClientForm, OrderForm,ServiceForm,UpdateOrderForm,TaskForm
from django.utils import timezone
from django.http.response import  JsonResponse
from django.views.generic.dates import MonthArchiveView, timezone_today
from datetime import timedelta
from django.db.models import Sum, Avg, Max, Min, Count, F
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('core:home')

class ClientView(LoginRequiredMixin,ListView):
    template_name = "clients.html"
    model = Client

    def get_context_data(self, **kwargs):
        context = super(ClientView, self).get_context_data(**kwargs)
        context['form'] = ClientForm
        search_area = self.request.GET.get('search-area') or ''
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

class ServiceView(LoginRequiredMixin,ListView):
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

class DelService(LoginRequiredMixin,DeleteView):
    model = Service
    success_url =reverse_lazy('core:services')
    template_name='serv_check_del.html'

class OrderView(LoginRequiredMixin,ListView):
    template_name = "order.html"
    model = Order
    orders=OrderService.objects.filter(ordered=False)
    ordering = ['paid', "-start_date"]

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['form'] = OrderForm(self.request.POST or None)
        search_area = self.request.GET.get('search-area') or ''
        if search_area:
            context['object_list'] = context['object_list'].filter(
                client__name__icontains=search_area)
        return context

    def post(self, request, *args, **kwargs):
        form = OrderForm()
        try:
            if request.method == "POST":
                form = OrderForm(request.POST)
                if form.is_valid():
                    form.save()
                   
                    self.orders.update(ordered=True)
                    return redirect('core:orders')
                else:
                    messages.warning(self.request, "You do not have an active order")
                    return redirect("core:orders")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:orders")
        except ValueError:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:orders")

def DetailOrder(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = UpdateOrderForm(request.POST or None, instance=order)
    if form.is_valid():
        form.save()
        return redirect('core:orders')
    return render(request, 'detail_order.html', {"order": order, 'form': form})

class DelOrder(LoginRequiredMixin,DeleteView):
    model = Order
    success_url =reverse_lazy('core:orders')
    template_name='order_check.html'

class OrderSummary(LoginRequiredMixin,ListView):
    model=OrderService
    template_name="summary.html"
    queryset=OrderService.objects.all().filter(ordered=False)   
    orders=OrderService.objects.filter(ordered=False)

    def get_context_data(self, **kwargs):
        context = super(OrderSummary, self).get_context_data(**kwargs)
        context['form'] = OrderForm(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        form = OrderForm()
        try:
            if request.method == "POST":
                form = OrderForm(request.POST)
                if form.is_valid():
                    form.save()
                   
                    self.orders.update(ordered=True)
                    return redirect('core:orders')
                else:
                    messages.warning(self.request, "You do not have an active order")
                    return redirect("core:summary")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:summary")
        except ValueError:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:summary")

def add_to_cart(request, pk):
    serv = get_object_or_404(Service, id=pk)
    order_item, created = OrderService.objects.get_or_create(
        service=serv,
        ordered=False
    )
    # check if the order item is in the order
    if OrderService.objects.filter(service__id=serv.id).exists():
        order_item.quantity += 1
        order_item.save()
        messages.info(request, "This item quantity was updated.")
        return redirect("core:summary")
    else:
        order_item.save()
        messages.info(request, "This item was added to your cart.")
        return redirect("core:summary")

def remove_from_cart(request, pk):
    serv = get_object_or_404(Service, id=pk)
   
    if OrderService.objects.filter(service__id=serv.id).exists():
        order_item= OrderService.objects.filter(ordered=False,service=serv)[0]    
        if order_item.quantity > 1:
            order_item.quantity -= 1
            order_item.save()
            return redirect("core:summary")
        else:
            order_item.delete()
            return redirect("core:summary")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:summary")

def SetPaid(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.paid = True
    order.order_date = timezone_today()
    order.save()
    return redirect("core:orders")

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
            paid=True, order_date__month=i).filter(order_date__lt=X + timedelta(days=93))

        for item in items:
            amount += (item.get_final_price())
        if items.exists():
            orders.append(amount)
            months.append(i)

    data = {
        "labels": labels[:len(months)],

        "default": orders,

    }
    return JsonResponse(data)

class HomeView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        profit = Order.objects.filter(paid=True)
        pending = Order.objects.filter(paid=False)
        count_client = Client.objects.count()
        count_service = Service.objects.count()
        total = profit.annotate(
            total=F("service__quantity") * F('service__service__price') + F('extra_price')).aggregate(Sum('total'))['total__sum']
        if not total:
            total=0
        context = {
            'total': total,
            'count': profit.count(),
            'count_client': count_client,
            'pending': pending.count(),
            "count_service": count_service
        }
        return render(request, 'admin.html', context)

class MonthOrderView(LoginRequiredMixin,MonthArchiveView):
    template_name = 'months.html'
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

        money_m = profit.annotate(
            total=F("service__quantity") * F('service__service__price') + F('extra_price')).aggregate(Sum('total'))['total__sum']
        money_y = profit_y.annotate(
            total=F("service__quantity") * F('service__service__price') + F('extra_price')).aggregate(Sum('total'))['total__sum']
        orders_months = self.object_list.count()
        
        
        context['money_m'] = money_m
        context['money_y'] = money_y
        context['count'] = str(orders_months)
        context['count_m'] = str(profit.count())
        context['count_p'] = str(orders_months - profit.count())
        return context

def SetPaidByDate(request, pk, year, month):
    order = get_object_or_404(Order, pk=pk)
    order.paid = True
    order.order_date = timezone_today()
    order.save()

    return redirect("core:orders-month", year, month)

class TodoListView(ListView):
    model = Task
    template_name='task.html'

    def get_context_data(self, **kwargs):
        context = super(TodoListView, self).get_context_data(**kwargs)
        context['form'] = TaskForm

        return context

    def post(self,request,*args,**kwargs):
        form=TaskForm
        try:
            if request.method == "POST":
                form = TaskForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('core:task')
        except ObjectDoesNotExist:
            
            return redirect("core:task")

class TaskUpdateView(UpdateView):
    model = Task    
    template_name='detail_task.html'
    success_url='core:task'
    form_class =TaskForm

def SetTaskDone(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.done = True
    task.save()
    return redirect("core:task")

class DelTask(LoginRequiredMixin,DeleteView):
    model = Task
    success_url =reverse_lazy('core:task')
    template_name='task_check_delete.html'
    
