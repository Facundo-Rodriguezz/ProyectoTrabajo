from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, MovimientoStockViewSet, ProductViewSet

from api.auth_views.JWTView import CustomTokenObtainPairView, CustomRefreshTokenView


# Configurar el DefaultRouter
router = routers.DefaultRouter()

# Registrar los ViewSets
router.register(r'users', UserViewSet)
router.register(r'product', ProductViewSet, basename='product')
router.register(r'movimientos-stock', MovimientoStockViewSet, basename='movimientos-stock')

# Definir las URLs
urlpatterns = [
    path('', include(router.urls)),  # Incluye todas las rutas registradas en el router
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomRefreshTokenView.as_view(), name='token_refresh'),
]
