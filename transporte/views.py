from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
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

    def create(self, request, *args, **kwargs):
        origem = request.data.get("bairro_origem")
        destino = request.data.get("bairro_destino")
        variacao = request.data.get("nome_variacao")
        if Rota.objects.filter(bairro_origem=origem, bairro_destino=destino, nome_variacao=variacao, status=True).exists():
            raise ValidationError({
                "success": False,
                "message": "Uma rota com a mesma origem e destino já está cadastrada e ativa."
            })
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = Rota.objects.get(pk=self.kwargs["pk"])
        except Rota.DoesNotExist:
            return Response({
                "success": False,
                "message": "A rota solicitada não foi encontrada"
            }, status=status.HTTP_404_NOT_FOUND)
        if not instance.status:
            return Response({
                "success": False,
                "message": "A rota já está desativada"
            }, status=status.HTTP_400_BAD_REQUEST)
        instance.status = False
        instance.save()
        self.perform_log_action(
            instance,
            action_flag=CHANGE,
            change_message=[{"action": "soft delete", "changes": [
                {"field": "is_active", "old_value": True, "new_value": False}
            ]}]
        )
        return Response({
            "success": True,
            "message": "Rota desativada com sucesso"
        }, status=status.HTTP_200_OK)

class HorarioOnibusViewSet(LoggableMixin, viewsets.ModelViewSet):
    queryset = HorarioOnibus.objects.all()
    serializer_class = HorarioOnibusSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'horarios_por_rota']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'], url_path='rota/(?P<rota_nome>[^/]+)')
    def horarios_por_rota(self, request, rota_nome=None):
        try:
            bairro_origem, bairro_destino = rota_nome.split('-')
        except ValueError:
            return Response({"success": False, "message": "Formato inválido para a rota. Use origem-destino."}, status=400)

        rota = Rota.objects.filter(
            bairro_origem__iexact=bairro_origem,
            bairro_destino__iexact=bairro_destino
        ).first()

        if not rota:
            return Response({"success": False, "message": "Rota não encontrada"}, status=404)

        horarios = HorarioOnibus.objects.filter(id_rota=rota)
        serializer = self.get_serializer(horarios, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        try:
            horario_onibus = HorarioOnibus.objects.get(pk=self.kwargs["pk"])
        except HorarioOnibus.DoesNotExist:
            return Response({
                "success": False,
                "message": "O horário de ônibus solicitado não foi encontrado."
            }, status=status.HTTP_404_NOT_FOUND)
        horario_onibus.delete()
        return Response({
            "success": True,
            "message": "Horário de ônibus desativado com sucesso."
        }, status=status.HTTP_200_OK)

class PontoTrajetoViewSet(LoggableMixin, viewsets.ModelViewSet):
    queryset = PontoTrajeto.objects.all()
    serializer_class = PontoTrajetoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

class PontoOnibusViewSet(LoggableMixin, viewsets.ModelViewSet):
    queryset = PontoOnibus.objects.all()
    serializer_class = PontoOnibusSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def destroy(self, request, *args, **kwargs):
        try:
            pontos_onibus = PontoOnibus.objects.get(pk=self.kwargs["pk"])
        except PontoOnibus.DoesNotExist:
            return Response({
                "success": False,
                "message": "O ponto de ônibus solicitado não foi encontrado."
            }, status=status.HTTP_404_NOT_FOUND)
        pontos_onibus.delete()
        return Response({
            "success": True,
            "message": "Ponto de ônibus desativado com sucesso."
        }, status=status.HTTP_200_OK)

class RotaPontoOnibusViewSet(LoggableMixin, viewsets.ModelViewSet):
    queryset = RotaPontoOnibus.objects.all()
    serializer_class = RotaPontoOnibusSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
