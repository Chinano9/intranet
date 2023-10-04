import csv
import django_filters.rest_framework

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from django.db.models import Q
from ..models import Empleado
from ..serializers import EmpleadoSerializer
from ..paginators import EmpleadoPagination
from ..filters import EmpleadoFilter

class EmpleadosLista(ListAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    pagination_class = EmpleadoPagination
    filter_backends = [SearchFilter, django_filters.rest_framework.DjangoFilterBackend, OrderingFilter]
    filterset_class = EmpleadoFilter
    search_fields = ['nombre', 'apellido_paterno', 'apellido_materno']
    ordering_fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'fecha_contratacion', 'fecha_nacimiento']
    ordering = ['-fecha_contratacion']
    """def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            queryset = self.queryset.filter(
                Q(nombre__icontains=query) |
                Q(apellido_paterno__istartswith=query) |
                Q(apellido_materno__istartswith=query)
            )
            return queryset
        return self.queryset"""


class EmpleadoCreate(APIView):
    def get(self, request, format=None):
        query = request.GET.get('query')
        empleados = Empleado.objects.all()

        if query:
            empleados = empleados.filter(
                Q(nombre__istartswith=query) |
                Q(apellido_paterno__istartswith=query) |
                Q(apellido_materno__istartswith=query)
            )

        paginator = EmpleadoPagination()
        page_data = paginator.paginate_queryset(empleados, request)
        serializer = EmpleadoSerializer(page_data, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = EmpleadoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmpleadoDetalles(APIView):
    def get_object(self, pk):
        try:
            return Empleado.objects.get(pk=pk)
        except Empleado.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        empleado = self.get_object(pk)
        serializer = EmpleadoSerializer(empleado)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EmpleadoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        empleado = self.get_object(pk)
        serializer = EmpleadoSerializer(empleado, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        empleado = self.get_object(pk)
        empleado.delete()
        return Response({"status": "200 OK"}, status=status.HTTP_204_NO_CONTENT)

class ExportarEmpleadoView (APIView):
    def get_object(self, pk):
        try:
            return Empleado.objects.get(pk=pk)
        except Empleado.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        empleado = self.get_object(pk)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{empleado.nombre}_{empleado.apellido_paterno}.csv"'

        writer = csv.writer(response)
        writer.writerow(["Id","Antiguedad en dias","Nombre","Apellido paterno","Apellido materno","Fecha de nacimiento","Fecha de contratacion","Foto","Ciudad de origen","Estado de origen","Ciudad de residencia","Estado de residencia","Calle","Numero de casa","Codigo postal","Estado civil","Email","Telefono de casa","Telefono celular","RFC","Seguro social","CURP","Sueldo por dia","Sueldo en texto","Foto url","Jefe directo","Puesto"])

        serializer = EmpleadoSerializer(empleado)
        writer.writerow(serializer.data.values())

        return response
        

class ExportarDBView (APIView):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="empleados.csv"'

        writer = csv.writer(response)
        writer.writerow(["Id","Antiguedad en dias","Nombre","Apellido paterno","Apellido materno","Fecha de nacimiento","Fecha de contratacion","Foto","Ciudad de origen","Estado de origen","Ciudad de residencia","Estado de residencia","Calle","Numero de casa","Codigo postal","Estado civil","Email","Telefono de casa","Telefono celular","RFC","Seguro social","CURP","Sueldo por dia","Sueldo en texto","Foto url","Jefe directo","Puesto"])

        queryset = Empleado.objects.all()
        serializer = EmpleadoSerializer(queryset, many=True)
        for empleado_data in serializer.data:
            writer.writerow(empleado_data.values())
             

        return response
 
