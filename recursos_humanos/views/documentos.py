import os

from django.http import FileResponse, Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Empleado
from ..utils.documentos import generar_kardex, generar_gafete, generar_contrato_det

RUTA_DOCUMENTOS = '../utils/out/'

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
            return Response({'error': f'Error al generar el kardex: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        archivo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), documento))
        
        # Verificar si el archivo existe
        if os.path.exists(archivo_path):
            # Enviar el archivo en la respuesta
            return FileResponse(open(archivo_path, 'rb'), as_attachment=True, headers={'Access-Control-Allow-Origin':'*'})

        # Si el archivo no existe, retornar una respuesta de error
        return Response({'detail': 'El archivo no se encontró.'}, status=status.HTTP_404_NOT_FOUND)

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
            return Response({'error': f'Error al generar el contrato: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        archivo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), documento))
        
        # Verificar si el archivo existe
        if os.path.exists(archivo_path):
            # Enviar el archivo en la respuesta
            return FileResponse(open(archivo_path, 'rb'), as_attachment=True)

        # Si el archivo no existe, retornar una respuesta de error
        return Response({'detail': 'El archivo no se encontró.'}, status=status.HTTP_404_NOT_FOUND)

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
            return Response({'error': f'Error al generar el gafete: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        archivo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), documento))
        
        # Verificar si el archivo existe
        if os.path.exists(archivo_path):
            # Enviar el archivo en la respuesta
            return FileResponse(open(archivo_path, 'rb'), as_attachment=True, headers={'Access-Control-Allow-Origin':'*'})

        # Si el archivo no existe, retornar una respuesta de error
        return Response({'detail': 'El archivo no se encontró.'}, status=status.HTTP_404_NOT_FOUND)


