from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Usuario (models.Model):
    user = models.CharField(primary_key = True, max_length=20)
    password = models.CharField(max_length=20)
    nombre = models.CharField(max_length=80)
    tipo = models.CharField(max_length=20)
    #Cliente, Empleado, Administrador
    def __str__(self):
        return self.user
    
    def to_dict(self):
        return {'user': self.user}
    
class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25, unique=True)
    fono = models.IntegerField(validators=[MinValueValidator(10000000), MaxValueValidator(99999999)])
    tipo = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre
    
class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.nombre
    
class ReservaHora(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    fecha_reserva = models.CharField(max_length=100)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self):
        return self.fecha_reserva
