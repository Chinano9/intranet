from rest_framework import serializers
from .models import Empleado
from django.utils.timezone import now

class EmpleadoSerializer (serializers.ModelSerializer):
    antiguedad_dias = serializers.SerializerMethodField()

    class Meta:
        model = Empleado
        fields = '__all__'

    def get_antiguedad_dias(self, obj):
        return (now().date() - obj.fecha_contratacion).days

class EmpleadoPaginadoSerializer (serializers.ModelSerializer):
    class Meta:
        model: Empleado 
