from django.db import models

# Create your models here.
class Planta (models.Model):
    nombre = models.CharField(max_length=20)
    

class Empleado (models.Model):
    uid = models.CharField(primary_key=True, max_length = 8)
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    fecha_contratacion = models.DateField()
    foto = models.FileField()
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    puesto = models.CharField(max_length=30)
    tel_casa = models.CharField(max_length=100)
    tel_cel = models.CharField(max_length=10)
    rfc = models.CharField(max_length=100)
    seguro_social = models.CharField(max_length=100)
    curp = models.CharField(max_length=100)
    sueldo_hora = models.IntegerField(default = 318)
    sueldo_texto = models.CharField(max_length=100)

