from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
urlpatterns = [
    path('puestos/', views.PuestoLista.as_view(), name='puestos'),
    path('puestos/nuevo/', views.PuestoCreate.as_view(), name='crear_puesto'),
    path('puestos/<int:pk>', views.PuestoDetalles.as_view(), name='detalles_puesto'),
    path('empleados/', views.EmpleadosLista.as_view(), name='empleados'),
    path('empleados/nuevo/', views.EmpleadoCreate.as_view(), name='crear_empleado'),
    path('empleados/<int:pk>', views.EmpleadoDetalles.as_view(), name='detalles_empleado'),
    path('empleados/documentos/kardex/<int:pk>', views.KardexView.as_view(), name='descargar_kardex'),
    path('empleados/documentos/contrato_determinado/<int:pk>', views.ContratoDeterminadoView.as_view(), name='descargar_contrato_determinado'),
    path('empleados/documentos/contrato_indeterminado/<int:pk>', views.ContratoIndeterminadoView.as_view(), name='descargar_contrato_indeterminado'),
    path('empleados/documentos/gafete/<int:pk>', views.GafeteView.as_view(), name='descargar_gafete'),
    path('empleados/documentos/exportar_csv/<int:pk>', views.ExportarEmpleadoView.as_view(), name='exportar_csv_empleado'),
    path('empleados/documentos/exportar_csv/', views.ExportarDBView.as_view(), name='exportar_csv'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # URL para obtener el token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # URL para refrescar el token
]
