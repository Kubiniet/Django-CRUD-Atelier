from django.db import models

# Create your models here.

class Cliente(models.Model):
    name = models.CharField(max_length=30)
    adress = models.CharField(max_length=30,verbose_name='La puta direccion')
    email = models.EmailField(blank=True,null=True)
    phone = models.CharField(max_length=10)
    phone = models.CharField(max_length=10 ,blank=True,null=True)
    def __str__(self):
        return self.name
    

class Seccion(models.Model):
    name = models.CharField(max_length=30)   
    
class Genre(models.Model):
    name = models.CharField(max_length=30)
   
class Servicio(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=6,decimal_places=2,null=True)
    genre = models.ForeignKey(Genre,null=True,on_delete=models.CASCADE)
    seccion= models.ForeignKey(Seccion,null=True,on_delete=models.CASCADE)    
    
    def __str__(self):
        return self.name

class Pedido(models.Model):
    numero = models.IntegerField(primary_key=True)
    fecha = models.DateField()
    entregado =models.BooleanField()
    pagado= models.BooleanField(default=False)
    servicio = models.ForeignKey(Servicio,null=True,blank=True,on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente,null=True,blank=True,on_delete=models.CASCADE)