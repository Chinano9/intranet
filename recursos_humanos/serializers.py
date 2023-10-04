from rest_framework import serializers
from .models import Empleado, Puesto, Planta
from django.utils.timezone import now

class PuestoSerializer (serializers.ModelSerializer):
    class Meta:
        model = Puesto
        fields = '__all__'

class PlantaSerializer (serializers.ModelSerializer):
    class Meta:
        model = Planta
        fields = '__all__'

class EmpleadoSerializer (serializers.ModelSerializer):
    antiguedad_dias = serializers.SerializerMethodField()

    class Meta:
        model = Empleado
        fields = '__all__'

    def get_antiguedad_dias(self, obj):
        return (now().date() - obj.fecha_contratacion).days


class EmpleadoPaginadoSerializer(serializers.ModelSerializer):
    puesto = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='nombre'
     )    
    class Meta:
        model = Empleado 
        fields = ['id', 'foto_url', 'nombre', 'email', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'fecha_contratacion', 'ciudad_residencia', 'estado_residencia', 'codigo_postal', 'puesto']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        print('AQUI SI EJECUTA')

        # Obtener la información del paginador proporcionada por DRF
        paginator = self.context.get('paginator')
        if paginator is not None:
            current_page = self.context['request'].query_params.get('page')
            if current_page is not None:
                data['pagina_actual'] = int(current_page)

            # Agregar información sobre la página siguiente y anterior si está disponible
            next_page = self.context['request'].query_params.get('page')
            if next_page is not None:
                data['next'] = int(next_page) + 1

            previous_page = self.context['request'].query_params.get('page')
            if previous_page is not None:
                data['prev'] = int(previous_page) - 1

            # Agregar el conteo total de empleados
            data['total_empleados'] = paginator.count

        # Personalizar la representación del puesto
        puesto_id = data['puesto_id']

        # Obtener el objeto Puesto correspondiente
        puesto_instance = Puesto.objects.get(pk=puesto_id)

        # Serializar el objeto Puesto
        puesto_serializer = PuestoSerializer(puesto_instance)
        puesto_data = puesto_serializer.data

        data['puesto'] = puesto_data
        return data
