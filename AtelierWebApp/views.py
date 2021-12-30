from django.http.response import HttpResponse
from django.shortcuts import render, HttpResponse,redirect
from .models import Cliente,Servicio,Pedido
from .forms import ClienteForm,PedidoForm
# Create your views here.

def home(request):
    clientes= Cliente.objects.all()
    
    return render(request,'Atelier/home.html',{"clientes":clientes})

def registrarCliente(request):
    name= request.POST['txtName']
    adress= request.POST['txtAdress']
    phone= request.POST['numPhone']
    phone2= request.POST['numPhone2']
    cliente = Cliente.objects.create(name=name, adress=adress, phone=phone)
    return redirect('/')
   
def eliminarCliente(request,pk):
    cliente= Cliente.objects.get(pk=pk)
    cliente.delete()
    return redirect('/')
    
def editarCliente(request,pk):
    cliente = Cliente.objects.get(pk=pk)
    return render(request,'Atelier/editarCliente.html',{ "cliente":cliente})
  
def conf_edit(request):
    Id= request.POST['txtId']
    name= request.POST['txtName']
    adress= request.POST['txtAdress']
    phone= request.POST['numPhone']
    phone2= request.POST['numPhone2']
    cliente = Cliente.objects.get(pk=Id)
    cliente.name=name
    cliente.adress=adress
    cliente.phone=phone
    cliente.phone2=phone2
    cliente.save()
    return redirect('/')
      

def servicios(request):
    servicios= Servicio.objects.all() 
    form = ClienteForm()
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('servicios')
    return render(request, 'Atelier/servicios.html',{ "servicios":servicios,'form': form})

def eliminarServicio(request,pk):
    servicio= Servicio.objects.get(pk=pk)
    servicio.delete()
    return redirect('/')
    
def editarCliente(request,pk):
    servicios= Servicio.objects.get(id=pk)
    form = ClienteForm(request.POST or None, instance=servicios)
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('servicios')
    return render(request,'Atelier/editarServicio.html',{ "servicios":servicios,'form': form})


def pedidos(request):
    pedidos = Pedido.objects.all()
    form= PedidoForm(request.POST)
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedidos')
        
    context = {'form': form,"pedidos":pedidos}
    
    return render(request,'Atelier/pedidos.html',context)

def eliminarPedido(request,pk):
    pedido= Pedido.objects.get(pk=pk)
    pedido.delete()
    return redirect('pedidos')

def blogs (request):
    
    return HttpResponse("Blogs")

def contacto(request):
    
    return HttpResponse("Contacto")