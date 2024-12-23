from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'rotas', views.RotaViewSet)
router.register(r'horarios', views.HorarioOnibusViewSet)
router.register(r'pontos_trajeto', views.PontoTrajetoViewSet)
router.register(r'pontos_onibus', views.PontoOnibusViewSet)
router.register(r'rotas_ponto_onibus', views.RotaPontoOnibusViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'subscription-notification', views.PushSubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
