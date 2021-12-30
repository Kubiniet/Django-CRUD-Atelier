from django.db import models

# Create your models here.

class Cliente(models.Model):
    name = models.CharField(max_length=30)
    adress = models.CharField(max_length=30,verbose_name='La puta direccion')
    email = models.EmailField(blank=True,null=True)
    phone = models.CharField(max_length=10,null=True)
    phone2 = models.CharField(max_length=10 ,blank=True,null=True)
    def __str__(self):
        return self.name
    

class Seccion(models.Model):
    name = models.CharField(max_length=30)  
    def __str__(self):
        return self.name 
    
class Genre(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
   
class Servicio(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6,decimal_places=2,null=True)
    genre = models.ForeignKey(Genre,null=True,on_delete=models.CASCADE)
    seccion= models.ForeignKey(Seccion,null=True,on_delete=models.CASCADE)    
    
    def __str__(self):
        return f"{self.name},{self.seccion},{self.genre}"

class Pedido(models.Model):
    numero = models.IntegerField(primary_key=True)
    fecha = models.DateField()
    entregado =models.BooleanField()
    pagado= models.BooleanField(default=False)
    servicio = models.ForeignKey(Servicio,null=True,blank=True,on_delete=models.CASCADE)
    servicio2 = models.ForeignKey(Servicio,null=True,blank=True,on_delete=models.CASCADE,related_name="servicio2")
    servicio3 = models.ForeignKey(Servicio,null=True,blank=True,on_delete=models.CASCADE,related_name="servicio3")
    cliente = models.ForeignKey(Cliente,blank=True,on_delete=models.CASCADE)
    
    def get_total_item_price(self):
        return self.servicio2.price * self.servicio.price
    
    def get_total(self):
        total = 0
        for order_item in self.all():
            total += order_item.get_total_item_price()