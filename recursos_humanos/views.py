from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Empleado
from .serializers import EmpleadoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

class EmpleadosLista(APIView):
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
        serializer = EmpleadoSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
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

    def patch(self, request, pk):
        empleado = self.get_object(pk)
        serializer = EmpleadoSerializer(empleado, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        empleado = self.get_object(pk)
        empleado.delete()
        return Response({"status":"200 0K"}, status=status.HTTP_200_OK) 
