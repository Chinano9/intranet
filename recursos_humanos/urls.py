from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from .views import empleados, puestos, plantas, documentos
urlpatterns = [
    path('puestos/', puestos.PuestoLista.as_view(), name='puestos'),
    path('puestos/nuevo/', puestos.PuestoCreate.as_view(), name='crear_puesto'),
    path('puestos/<int:pk>', puestos.PuestoDetalles.as_view(), name='detalles_puesto'),
    path('empleados/', empleados.EmpleadosLista.as_view(), name='empleados'),
    path('empleados/nuevo/', empleados.EmpleadoCreate.as_view(), name='crear_empleado'),
    path('empleados/<int:pk>', empleados.EmpleadoDetalles.as_view(), name='detalles_empleado'),
    path('empleados/documentos/kardex/<int:pk>', documentos.KardexView.as_view(), name='descargar_kardex'),
    path('empleados/documentos/contrato_determinado/<int:pk>', documentos.ContratoDeterminadoView.as_view(), name='descargar_contrato_determinado'),
    path('empleados/documentos/contrato_indeterminado/<int:pk>', documentos.ContratoIndeterminadoView.as_view(), name='descargar_contrato_indeterminado'),
    path('empleados/documentos/gafete/<int:pk>', documentos.GafeteView.as_view(), name='descargar_gafete'),
    path('empleados/documentos/exportar_csv/<int:pk>', empleados.ExportarEmpleadoView.as_view(), name='exportar_csv_empleado'),
    path('empleados/documentos/exportar_csv/', empleados.ExportarDBView.as_view(), name='exportar_csv'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # URL para obtener el token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # URL para refrescar el token
]
