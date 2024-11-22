from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Rota, HorarioOnibus, Log, PontoTrajeto, PontoOnibus, RotaPontoOnibus
from .serializers import RotaSerializer, HorarioOnibusSerializer, LogSerializer, PontoTrajetoSerializer, PontoOnibusSerializer, RotaPontoOnibusSerializer
from django.contrib.admin.models import CHANGE

from transporte.logging import LoggableMixin

class RotaViewSet(LoggableMixin, viewsets.ModelViewSet):
    queryset = Rota.objects.filter(status=True)
    serializer_class = RotaSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Ações de leitura (GET)
            return [AllowAny()]  # Qualquer usuário pode acessar
        return [IsAuthenticated()] # Outros métodos precisam de autenticação
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.status:
            response_data = {
                "success": False,
                "message": "A rota já está desativada"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        instance.status = False
        instance.save()

        self.perform_log_action(
            instance,
            action_flag=CHANGE,
            change_message=[{"action": "soft delete", "changes": [
                {"field": "is_active", "old_value": True, "new_value": False}
            ]}]
        )
        response_data = {
            "success": True,
            "message": "Rota desativada com sucesso"
        }
        return Response(response_data, status=status.HTTP_200_OK)

class HorarioOnibusViewSet(viewsets.ModelViewSet):
    queryset = HorarioOnibus.objects.all()
    serializer_class = HorarioOnibusSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer

class PontoTrajetoViewSet(viewsets.ModelViewSet):
    queryset = PontoTrajeto.objects.all()
    serializer_class = PontoTrajetoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

class PontoOnibusViewSet(viewsets.ModelViewSet):
    queryset = PontoOnibus.objects.all()
    serializer_class = PontoOnibusSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

class RotaPontoOnibusViewSet(viewsets.ModelViewSet):
    queryset = RotaPontoOnibus.objects.all()
    serializer_class = RotaPontoOnibusSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
