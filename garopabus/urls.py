"""
URL configuration for garopabus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from transporte import views, admin

# Criar o esquema do Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="GaropaBus API",
        default_version='v1',
        description="API para o sistema de transporte GaropaBus",
        terms_of_service="https://www.seusite.com/terms/",
        contact=openapi.Contact(email="contato@seusite.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Configurar o roteador para os ViewSets
router = DefaultRouter()
router.register(r'rotas', views.RotaViewSet)
router.register(r'horarios', views.HorarioOnibusViewSet)
router.register(r'logs', views.LogViewSet)
router.register(r'pontos_trajeto', views.PontoTrajetoViewSet)
router.register(r'pontos_onibus', views.PontoOnibusViewSet)
router.register(r'rotas_ponto_onibus', views.RotaPontoOnibusViewSet)

# Definir as URLs
urlpatterns = [
    path('api/', include(router.urls)),  # Inclui as rotas da API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Para obter o token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
