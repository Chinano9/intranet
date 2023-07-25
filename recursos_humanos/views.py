from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Empleado
from .serializers import EmpleadoSerializer

# Create your views here.

class EmpleadosLista(APIView):
    def get(self, request, format=None):
        empleados = Empleados.objects.all()
        serializer = EmpleadoSerializer(empleados)

        return Response(serializer.data)


class EmpleadoDetalles(APIView):
    def get_object(self, pk):
        try:
            return Empleado.objects.get(pk=pk)
        except Empleado.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        empleado = self.get_object(pk)
        serializer = EmpleadoSerializer(empleado)
        return Response(serializer)

    def put(self, request, pk):
        empleado = self.get_object(pk)
        serializer = EmpleadoSerializer(empleado, data = request.data)
        if serializer.isValid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        empleado = self.get_object(pk)
        empleado.delete()
