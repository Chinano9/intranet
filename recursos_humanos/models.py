from django.db import models

# Create your models here.
class Planta (models.Model):
    nombre = models.CharField(max_length=20)
    

class Empleado (models.Model):
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(blank=True ,max_length=50)
    fecha_nacimiento = models.DateField()
    fecha_contratacion = models.DateField()
    foto = models.FileField(blank = True)
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=5)
    email = models.CharField(max_length=100)
    puesto = models.CharField(max_length=30)
    tel_casa = models.CharField(blank=True,max_length=100)
    tel_cel = models.CharField(max_length=10)
    rfc = models.CharField(max_length=100)
    seguro_social = models.CharField(max_length=100)
    curp = models.CharField(max_length=100)
    sueldo_dia = models.IntegerField(default = 318)
    sueldo_texto = models.CharField(max_length=100)

class Departamento(models.Model):
    nombre = models.CharField(max_length = 20)
    jefe = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
