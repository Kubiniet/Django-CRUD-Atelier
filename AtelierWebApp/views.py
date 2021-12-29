from django.http.response import HttpResponse
from django.shortcuts import render, HttpResponse,redirect
from .models import Cliente,Servicio
from .forms import ClienteForm
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
      
"""def servicios(request):
    servicios= Servicio.objects.all()    
    return render(request,'Atelier/servicios.html',{ "servicios":servicios})"""

def servicios(request):
    servicios= Servicio.objects.all() 
    form = ClienteForm()
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('servicios')
    return render(request, 'Atelier/servicios.html',{ "servicios":servicios,'form': form})

def tienda(request):
    
    return HttpResponse("Tienda")


def blogs (request):
    
    return HttpResponse("Blogs")

def contacto(request):
    
    return HttpResponse("Contacto")