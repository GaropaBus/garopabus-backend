from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import Rota, HorarioOnibus, PontoTrajeto, PontoOnibus, RotaPontoOnibus
from .serializers import RotaSerializer, HorarioOnibusSerializer, PontoTrajetoSerializer, PontoOnibusSerializer, RotaPontoOnibusSerializer
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
        if self.action in ['list', 'retrieve', 'horarios_por_rota']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'], url_path='(?P<rota_nome>[^/]+)')
    def horarios_por_rota(self, request, rota_nome=None):
        try:
            bairro_origem, bairro_destino = rota_nome.split('-')
            partida_normalizada = bairro_origem.replace('-', ' ').lower()
            chegada_normalizada = bairro_destino.replace('-', ' ').lower()
        except ValueError:
            return Response({"error": "Formato inválido para a rota. Use origem-destino."}, status=400)

        rota = Rota.objects.filter(
            bairro_origem__iexact=partida_normalizada,
            bairro_destino__iexact=chegada_normalizada
        ).first()

        if not rota:
            return Response({"error": "Rota não encontrada"}, status=404)

        horarios = HorarioOnibus.objects.filter(id_rota=rota)
        serializer = self.get_serializer(horarios, many=True)
        return Response(serializer.data)

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
