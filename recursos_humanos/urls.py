from django.urls import path

from . import views
urlpatterns = [
    path('empleados', views.EmpleadosLista.as_view(), name='empleados'),
    path('empleados/<str:uid>', views.EmpleadoDetalles.as_view(), name='detalles_empleado'),
]
