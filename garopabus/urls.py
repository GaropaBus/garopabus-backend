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
from django.contrib.auth.decorators import login_required
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from transporte import views
from transporte.views import validate_token

# Criar o esquema do Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="GaropaBus API",
        default_version='v1',
        description="API para o sistema de transporte GaropaBus",
        terms_of_service="https://garopabus.uk/terms/",
        contact=openapi.Contact(email="contato@garopabus.uk"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

# Configurar o roteador para os ViewSets
router = DefaultRouter()
router.register(r'rotas', views.RotaViewSet)
router.register(r'horarios', views.HorarioOnibusViewSet)
router.register(r'pontos_trajeto', views.PontoTrajetoViewSet)
router.register(r'pontos_onibus', views.PontoOnibusViewSet)
router.register(r'rotas_ponto_onibus', views.RotaPontoOnibusViewSet)

# Definir as URLs
urlpatterns = [
    path('api/', include(router.urls)),  # Inclui as rotas da API

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Para obter o token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/validate/', validate_token, name='validate_token'),

    path('swagger/', login_required(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    path('redoc/', login_required(schema_view.with_ui('redoc', cache_timeout=0)), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('accounts/', include('rest_framework.urls')),
]
