from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, MovimientoStockViewSet, ProductViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Configurar el DefaultRouter
router = routers.DefaultRouter()

# Registrar los ViewSets
router.register(r'users', UserViewSet)
router.register(r'product', ProductViewSet, basename='product')
router.register(r'movimientos-stock', MovimientoStockViewSet, basename='movimientos-stock')

# Definir las URLs
urlpatterns = [
    path('', include(router.urls)),  # Incluye todas las rutas registradas en el router
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # Autenticación de la API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtener el token JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refrescar el token JWT
]
