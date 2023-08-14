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
        model = Empleado 
        fields = ['id', 'foto_url', 'nombre', 'email', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'fecha_contratacion', 'ciudad', 'estado', 'codigo_postal', 'puesto']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Obtener la información del paginador proporcionada por DRF
        paginator = self.context.get('paginator')
        if paginator is not None:
            current_page = request.query_params.get('page')
            if current_page is not None:
                data['current_page'] = int(current_page)
            # Agregar información sobre la página siguiente y anterior si está disponible
            next_page = self.context['request'].GET.get('page')  # Obtener el número de página actual
            if next_page is not None:
                data['next_page'] = int(next_page) + 1

            previous_page = self.context['request'].GET.get('page')  # Obtener el número de página actual
            if previous_page is not None:
                data['previous_page'] = int(previous_page) - 1

            # Agregar el conteo total de empleados
            data['total_empleados'] = paginator.count

        return data

