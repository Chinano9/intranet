import django_filters
from .models import Empleado

class EsJefeFilter(django_filters.BooleanFilter):
    def filter(self, queryset, value):
        if value is None:
            return queryset

        if value:
            return queryset.filter(puesto__nombre__icontains='LÍDER')
        else:
            return queryset.exclude(puesto__nombre__icontains='LÍDER')


class EmpleadoFilter(django_filters.FilterSet):
    es_jefe = EsJefeFilter(field_name='es_jefe', label='Es Jefe')
    class Meta:
        model = Empleado
        fields = {
            'puesto__id': ['exact'],
            'fecha_contratacion': ['gte', 'lte'],
            # Agrega otros campos de filtro según sea necesario
        }
