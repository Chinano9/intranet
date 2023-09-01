import django_filters.rest_framework
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.http import Http404, FileResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Empleado, Puesto
from .serializers import EmpleadoSerializer, EmpleadoPaginadoSerializer, PuestoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

import csv
import os

from .utils.documentos import generar_kardex, generar_gafete

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

        try:
            generar_kardex(empleado.__dict__, documento)
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


class EmpleadoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def __init__(self):
        # Agrega una variable para almacenar el parámetro de búsqueda
        self.query = None
        super().__init__()

    def get_paginated_response(self, data):
        #serializer = EmpleadoPaginadoSerializer(data, many=True)
        return Response({
            'pagina_actual': self.page.number,
            'total_paginas': self.page.paginator.num_pages,
            'total_empleados': self.page.paginator.count,
            'next': self.page.number + 1 if (self.page.number + 1) <= self.page.paginator.num_pages else None,
            'prev': self.page.number - 1,
            'results': data,
        })

class EmpleadosLista(ListAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoPaginadoSerializer
    pagination_class = EmpleadoPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    
    def get_queryset(self):
        # Obtenemos el queryset original
        queryset = super().get_queryset()

        # Obtenemos el parámetro de búsqueda 'query' de la URL
        query = self.request.GET.get('query')

        # Si hay un parámetro de búsqueda, filtramos el queryset
        if query:
            queryset = queryset.filter((Q(nombre__icontains=query) | 
                                       Q(apellido_paterno__istartswith=query) |
                                       Q(apellido_materno__istartswith=query)))

        return queryset

    def get(self, request, format=None):
        # Obtenemos el queryset filtrado y paginado
        queryset = self.get_queryset()
        page_data = self.paginate_queryset(queryset)
        serializer = EmpleadoSerializer(page_data, many=True)
        return self.get_paginated_response(serializer.data)


class EmpleadoCreate(APIView):
#    authentication_classes = [JWTAuthentication]
#    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        empleados = Empleado.objects.all()

        # Busqueda de empleado por nombre, o apellido
        query = request.GET.get('query')
        if query:
            empleados = empleados.filter(Q(nombre__istartswith=query) | 
                                         Q(apellido_paterno__istartswith=query)|
                                         Q(apellido_materno__istartswith=query))

        paginator = Paginator(empleados,10)
        page_number = request.GET.get('page')
        page_data = paginator.get_page(page_number)
        serializer = EmpleadoSerializer(page_data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        #request.data['puesto'] = Puesto
        serializer = EmpleadoSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



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
        serializer = EmpleadoSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        empleado = self.get_object(pk)
        serializer = EmpleadoSerializer(empleado, data = request.data, partial=True)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        empleado = self.get_object(pk)
        empleado.delete()
        return Response({"status":"200 0K"}, status=status.HTTP_200_OK) 

class PuestoLista (ListAPIView):
    queryset = Puesto.objects.all()
    serializer_class = PuestoSerializer

class ExportarEmpleadoView (APIView):
    def get_object(self, pk):
        try:
            return Empleado.objects.get(pk=pk)
        except Empleado.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        empleado = self.get_object(pk)

        writer = csv.writer(response)
        writer.writerow(['ID', 'Nombre', 'Apellido', 'Foto URL'])  # Encabezado

        for empleado in empleados:
            writer.writerow([
                empleado.id,
                empleado.nombre,
                empleado.apellido,
                empleado.foto_url
            ])

        response = Response(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="empleados.csv"'

        writer = csv.DictWriter(response, fieldnames=data[0].keys())
        writer.writerows(data)
    
        return 
        

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
