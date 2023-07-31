from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
urlpatterns = [
    path('empleados/', views.EmpleadosLista.as_view(), name='empleados'),
    path('empleados/<int:pk>', views.EmpleadoDetalles.as_view(), name='detalles_empleado'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # URL para obtener el token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # URL para refrescar el token
]
