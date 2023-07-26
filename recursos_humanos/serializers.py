from rest_framework import serializers
from .models import Empleado
from django.utils.timezone import now

class EmpleadoSerializer (serializers.ModelSerializer):
    antiguedad = serializers.SerializerMethodField()

    class Meta:
        model = Empleado
        fields = '__all__'

    def get_antiguedad(self, obj):
        return (now() - obj.fecha_contratacion).days

