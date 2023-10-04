import django_filters.rest_framework

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from ..models import Planta
from ..serializers import PlantaSerializer
from ..paginators import PlantaPagination

class PuestoLista (ListAPIView):
    queryset = Planta.objects.all()
    serializer_class = PlantaSerializer
    pagination_class = PlantaPagination
    filter_backends = [SearchFilter, django_filters.rest_framework.DjangoFilterBackend, OrderingFilter]
    search_fields = ['ciudad']


class PuestoCreate (APIView):
    def post(self, request, format=None):
        serializer = PlantaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PuestoDetalles(APIView):
    def get_object(self, pk):
        try:
            return Planta.objects.get(pk=pk)
        except Planta.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        puesto = self.get_object(pk)
        serializer = PlantaSerializer(puesto)
        return Response(serializer.data)

    def patch(self, request, pk):
        puesto = self.get_object(pk)
        serializer = PlantaSerializer(puesto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        empleado = self.get_object(pk)
        empleado.delete()
        return Response({"status": "200 OK"}, status=status.HTTP_204_NO_CONTENT)
