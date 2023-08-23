from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.
class Planta (models.Model):
    nombre = models.CharField(max_length=20)
    
# TODO: DAR DE ALTA NUEVOS PUESTOS
class Empleado (models.Model):
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(blank=True ,max_length=50)
    # FORMATO DE FECHA DD/MMM/YYYY
    fecha_nacimiento = models.DateField()
    fecha_contratacion = models.DateField()
    foto = models.ImageField(upload_to='',blank = True)
    ciudad_origen = models.CharField(blank=True,max_length=100)
    estado_origen = models.CharField(blank=True,max_length=100)
    ciudad_residencia = models.CharField(max_length=100)
    estado_residencia = models.CharField(max_length=100)
    calle = models.CharField(max_length=100)
    num_casa = models.CharField(max_length=10)
    codigo_postal = models.CharField(max_length=5)
    jefe_directo = models.ForeignKey('self', null=True ,blank = True, on_delete=models.CASCADE)
    # FIX: TURNO, FALTA TURNO!!!!!!!!!!!!!!!!!!!
    #casado, soltero, divorciado, etc...
    estado_civil = models.CharField(blank = True, max_length = 40)
    email = models.CharField(max_length=100)
    puesto = models.ForeignKey('Puesto', on_delete=models.CASCADE)
    tel_casa = models.CharField(blank=True, max_length=100)
    tel_cel = models.CharField(max_length=10)
    rfc = models.CharField(max_length=100)
    seguro_social = models.CharField(max_length=100)
    curp = models.CharField(max_length=100)
    sueldo_dia = models.IntegerField(default = 318)
    sueldo_texto = models.CharField(max_length=100)
    foto_url = models.CharField(max_length=255, blank=True)  # Campo para almacenar la URL de la foto

    def save(self, *args, **kwargs):
        if self.foto:
            self.foto_url = self.get_absolute_url(self.foto)
        super().save(*args, **kwargs)

    def get_absolute_url(self, path):
        base_url = settings.BASE_URL
        return f"{base_url}fotos/{path}"

class Departamento(models.Model):
    nombre = models.CharField(max_length = 20)
    jefe = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)

class Puesto(models.Model):
    nombre = models.CharField(max_length=20)
    responsabilidad = models.CharField(max_length=255)

