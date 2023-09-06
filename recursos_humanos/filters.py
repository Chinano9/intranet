import django_filters
from .models import Empleado

class EmpleadoFilter(django_filters.FilterSet):
    class Meta:
        model = Empleado
        fields = {
            'puesto__id': ['exact'],
            'fecha_contratacion': ['gte', 'lte'],
            # Agrega otros campos de filtro según sea necesario
        }
