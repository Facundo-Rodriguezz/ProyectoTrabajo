from django.urls import path, include
from rest_framework import routers
from .views import ProductListCreateView,UserViewSet
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'product', UserViewSet)

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
