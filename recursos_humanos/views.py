import django_filters.rest_framework
import datetime
from rest_framework.filters import SearchFilter, OrderingFilter
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.http import Http404, FileResponse
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

import csv
import os

from .utils.documentos import generar_kardex, generar_gafete, generar_contrato_det
from .serializers import EmpleadoSerializer, EmpleadoPaginadoSerializer, PuestoSerializer
from .paginators import EmpleadoPagination, PuestoPagination
from .filters import EmpleadoFilter
from .models import Empleado, Puesto

RUTA_DOCUMENTOS = 'utils/out/'

class KardexView(APIView):
    def get_object(self, pk):
        try:
            return Empleado.objects.get(pk=pk)
        except Empleado.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        # Ruta al archivo que deseas enviar
        documento = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.join(RUTA_DOCUMENTOS,'kardex.pdf')))
        
        empleado = self.get_object(pk)

        try:
            generar_kardex(empleado.__dict__, documento)
        except Exception as e:
            return Response({'error': f'Error al generar el kardex: {e}'}, status=500)

        archivo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), documento))
        
        # Verificar si el archivo existe
        if os.path.exists(archivo_path):
            # Enviar el archivo en la respuesta
            return FileResponse(open(archivo_path, 'rb'), as_attachment=True, headers={'Access-Control-Allow-Origin':'*'})

        # Si el archivo no existe, retornar una respuesta de error
        return Response({'detail': 'El archivo no se encontró.'}, status=404)

class ContratoDeterminadoView(APIView):
    def get_object(self, pk):
        try:
            return Empleado.objects.get(pk=pk)
        except Empleado.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        # Ruta al archivo que deseas enviar
        documento = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.join(RUTA_DOCUMENTOS,'contrato.pdf')))
        
        empleado = self.get_object(pk)
        puesto = empleado.puesto

        datos_empleado = {
            'ciudad': f'{empleado.planta.ciudad} {empleado.planta.abreviatura_estado}',
            'hoy': datetime.datetime.now(),
            'nombre_empleado': f'{empleado.nombre} {empleado.apellido_paterno} {empleado.apellido_materno}',
            'origen_empleado': f'{empleado.ciudad_origen} {empleado.estado_origen}',
            'contratacion': empleado.fecha_contratacion,
            'puesto_empleado': puesto.nombre,
            'salario_empleado':empleado.salario,
            'salario_texto_empleado':empleado.salario_texto,
        }

        try:
            generar_contrato_det(datos_empleado, documento)
        except Exception as e:
            return Response({'error': f'Error al generar el contrato: {e}'}, status=500)

        archivo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), documento))
        
        # Verificar si el archivo existe
        if os.path.exists(archivo_path):
            # Enviar el archivo en la respuesta
            return FileResponse(open(archivo_path, 'rb'), as_attachment=True)

        # Si el archivo no existe, retornar una respuesta de error
        return Response({'detail': 'El archivo no se encontró.'}, status=404)

    pass

class ContratoIndeterminadoView(APIView):
    pass

class GafeteView(APIView):
    def get_object(self, pk):
        try:
            return Empleado.objects.get(pk=pk)
        except Empleado.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        # Ruta al archivo que deseas enviar
        documento = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.join(RUTA_DOCUMENTOS,'gafete.pdf')))
        
        empleado = self.get_object(pk)
        puesto = empleado.puesto

        datos_empleado = {
            'foto': empleado.foto.name,
            'nombre': empleado.nombre,
            'apellido_paterno': empleado.apellido_paterno,
            'apellido_materno': empleado.apellido_materno,
            'id': empleado.id,
            'curp': empleado.curp,
            'seguro_social': empleado.seguro_social,
            'puesto_nombre': puesto.nombre,
            'puesto_responsabilidad': puesto.responsabilidad,
        }

        try:
            generar_gafete(datos_empleado, documento)
        except Exception as e:
            print(f"Error al generar el gafete: {e}")
            return Response({'error': f'Error al generar el gafete: {e}'}, status=500)

        archivo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), documento))
        
        # Verificar si el archivo existe
        if os.path.exists(archivo_path):
            # Enviar el archivo en la respuesta
            return FileResponse(open(archivo_path, 'rb'), as_attachment=True, headers={'Access-Control-Allow-Origin':'*'})

        # Si el archivo no existe, retornar una respuesta de error
        return Response({'detail': 'El archivo no se encontró.'}, status=404)


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
            return Response(serializer.data)
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
    pass

class PuestoLista (ListAPIView):
    queryset = Puesto.objects.all()
    serializer_class = PuestoSerializer
    pagination_class = PuestoPagination
    filter_backends = [SearchFilter, django_filters.rest_framework.DjangoFilterBackend, OrderingFilter]
    search_fields = ['nombre']


class PuestoCreate (APIView):
    def post(self, request, format=None):
        serializer = PuestoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PuestoDetalles(APIView):
    def get_object(self, pk):
        try:
            return Puesto.objects.get(pk=pk)
        except Puesto.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        puesto = self.get_object(pk)
        serializer = PuestoSerializer(puesto)
        return Response(serializer.data)

    def patch(self, request, pk):
        puesto = self.get_object(pk)
        serializer = PuestoSerializer(puesto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        empleado = self.get_object(pk)
        empleado.delete()
        return Response({"status": "200 OK"}, status=status.HTTP_204_NO_CONTENT)
