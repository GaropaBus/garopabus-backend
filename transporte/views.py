from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import status
from django.db import transaction
from garopabus.settings import TYPE_ENV, VAPID_PUBLIC_KEY
from .models import Rota, HorarioOnibus, PontoTrajeto, PontoOnibus, RotaPontoOnibus, Notification, PushSubscription
from .serializers import RotaSerializer, HorarioOnibusSerializer, PontoTrajetoSerializer, PontoOnibusSerializer, RotaPontoOnibusSerializer, NotificationSerializer, PushSubscriptionSerializer
from .filters import RotaFilter
from .logging import LoggableMixin
from .utils import send_push_notification, normalize_route_name, obter_rota_principal_e_variacoes
from django.contrib.admin.models import DELETION, CHANGE


class RotaViewSet(LoggableMixin, viewsets.ModelViewSet):
    queryset = Rota.objects.filter(status=True)
    serializer_class = RotaSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:  # Ações de leitura (GET)
            # Apenas esses métodos precisam de autenticação
            return [IsAuthenticated()]
        return [AllowAny()]  # Qualquer usuário pode acessar

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = sorted(
            queryset, key=lambda x: (
                min(x.bairro_origem, x.bairro_destino),
                max(x.bairro_origem, x.bairro_destino),
            )
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='filtrado(?:/(?P<tipo>[^/]+))?')
    def listar_trajetos(self, request, tipo=None):
        """
        Lista trajetos com filtragem opcional pelo tipo.
        /api/rotas/filtrado/ -> Todos os tipos"
        /api/rotas/filtrado/variacao/ -> Apenas tipo "variacao"
        /api/rotas/filtrado/principal/ -> Apenas tipo "principal"
        """
        if tipo == "variacao":
            todas_rotas = Rota.objects.filter(
                status=True, tipo="variacao")  # Apenas "variacao"
        elif tipo == "principal":
            todas_rotas = Rota.objects.filter(
                status=True, tipo="principal")  # Apenas "principal"
        else:
            todas_rotas = Rota.objects.filter(status=True)

        sentido_garopaba = []
        sentido_bairros = []

        for rota in todas_rotas:
            if rota.bairro_origem == "Garopaba" and rota.bairro_destino != "Garopaba":
                sentido_bairros.append(rota)
            elif rota.bairro_destino == "Garopaba" and rota.bairro_origem != "Garopaba":
                sentido_garopaba.append(rota)

        sentido_garopaba = sorted(
            sentido_garopaba, key=lambda x: (x.bairro_origem, x.bairro_destino)
        )
        sentido_bairros = sorted(
            sentido_bairros, key=lambda x: (x.bairro_origem, x.bairro_destino)
        )

        # Ajustar para que rotas com destinos opostos fiquem próximas
        sentido_garopaba = sorted(
            sentido_garopaba, key=lambda x: (
                min(x.bairro_origem, x.bairro_destino), max(x.bairro_origem, x.bairro_destino))
        )
        sentido_bairros = sorted(
            sentido_bairros, key=lambda x: (
                min(x.bairro_origem, x.bairro_destino), max(x.bairro_origem, x.bairro_destino))
        )

        sentido_garopaba_data = RotaSerializer(
            sentido_garopaba, many=True).data
        sentido_bairros_data = RotaSerializer(sentido_bairros, many=True).data

        response_data = {
            "sentido_garopaba": sentido_garopaba_data,
            "sentido_bairros": sentido_bairros_data
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='filtrar')
    def filtrar(self, request, *args, **kwargs):
        filterset = RotaFilter(data=request.data, queryset=self.queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)

        serializer = self.get_serializer(filterset.qs, many=True)
        return Response(serializer.data)

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
            instance=instance,
            action_flag=DELETION,
            log_data={
                'changes': [
                    {'field': 'status', 'from': True, 'to': False}
                ]
            }
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
        rota_principal, rotas_variacoes, erro = obter_rota_principal_e_variacoes(
            rota_nome)
        if erro:
            return Response(erro, status=400)

        todas_rotas = [rota_principal] + list(rotas_variacoes)
        horarios = HorarioOnibus.objects.filter(
            id_rota__in=todas_rotas).order_by('hora_partida')

        dias_uteis = []
        fim_semana = []

        for horario in horarios:
            tipo_variacao = (
                "Direto" if horario.id_rota == rota_principal.id
                else (horario.id_rota.nome_variacao if horario.id_rota.nome_variacao is not None else None)
            )
            horario_data = {
                "id": horario.id,
                "dia_semana": horario.dia_semana,
                "hora_partida": horario.hora_partida.strftime("%H:%M"),
                "hora_chegada": horario.hora_chegada.strftime("%H:%M"),
                "id_rota": horario.id_rota.id,
                "tipo_variacao": tipo_variacao
            }
            if horario.dia_semana == "dia_util":
                dias_uteis.append(horario_data)
            else:
                fim_semana.append(horario_data)

        resultado = {
            "dias_uteis": dias_uteis,
            "fim_semana": fim_semana
        }

        return Response(resultado, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            horario_onibus = HorarioOnibus.objects.get(
                pk=self.kwargs["pk"])
        except HorarioOnibus.DoesNotExist:
            return Response({
                "success": False,
                "message": "O horário de ônibus solicitado não foi encontrado."
            }, status=status.HTTP_404_NOT_FOUND)
        super().destroy(request, *args, **kwargs)
        return Response({
            "success": True,
            "message": "Horário de ônibus desativado com sucesso."
        }, status=status.HTTP_200_OK)


class PontoTrajetoViewSet(LoggableMixin, viewsets.ModelViewSet):
    queryset = PontoTrajeto.objects.all()
    serializer_class = PontoTrajetoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'pontos_por_rota_nome', 'pontos_por_rota_id']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        id_rota = request.data.get('id_rota')
        if not id_rota:
            return Response(
                {"sucess": False, "detail": "O campo 'id_rota' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )
        ultima_ordem = PontoTrajeto.objects.filter(
            id_rota=id_rota).order_by('-ordem').first()

        nova_ordem = (ultima_ordem.ordem + 1) if ultima_ordem else 1
        data = request.data.copy()
        data['ordem'] = nova_ordem
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='rota-nome/(?P<rota_nome>[^/]+)')
    def pontos_por_rota_nome(self, request, rota_nome=None):
        rota_principal, rotas_variacoes, erro = obter_rota_principal_e_variacoes(
            rota_nome)
        if erro:
            return Response(erro, status=400)

        rotas_relacionadas = [rota_principal] + list(rotas_variacoes)
        pontos_por_variacao = {}
        for rota in rotas_relacionadas:
            pontos = PontoTrajeto.objects.filter(
                id_rota=rota).order_by('ordem')
            pontos_serializados = PontoTrajetoSerializer(
                pontos, many=True).data
            nome_variacao = rota.nome_variacao if rota.nome_variacao else "principal"

            if nome_variacao not in pontos_por_variacao:
                nome_variacao = normalize_route_name(nome_variacao)
                pontos_por_variacao[nome_variacao] = []

            pontos_por_variacao[nome_variacao].extend(pontos_serializados)
        return Response(pontos_por_variacao, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='rota-id/(?P<rota_id>[^/]+)')
    def pontos_por_rota_id(self, request, rota_id=None):
        try:
            rota = Rota.objects.get(id=rota_id)
        except Rota.DoesNotExist:
            return Response({"success": False, "message": "A rota solicitada não foi encontrada"}, status=404)

        pontos = PontoTrajeto.objects.filter(id_rota=rota).order_by('ordem')
        pontos_serializados = PontoTrajetoSerializer(pontos, many=True).data

        return Response(pontos_serializados, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='editar-em-massa')
    @transaction.atomic
    def editar_em_massa(self, request):
        """
        Endpoint para edição em massa de pontos de trajeto.
        """
        pontos = request.data

        if not isinstance(pontos, list):
            return Response(
                {"success": False, "detail": "O payload deve ser uma lista de pontos."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not pontos:
            return Response(
                {"success": False, "detail": "A lista de pontos está vazia."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Pega o id_rota do primeiro ponto para validação
        id_rota = pontos[0].get('id_rota')

        try:
            rota = Rota.objects.get(id=id_rota)

            # Captura o estado anterior dos pontos para logging
            pontos_anteriores = list(PontoTrajeto.objects.filter(
                id_rota=rota).order_by('ordem').values(
                'id', 'ordem', 'latitude', 'longitude', 'id_rota'
            ))
        except Rota.DoesNotExist:
            return Response(
                {"success": False, "detail": "ID Rota não encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Valida se todos os pontos são da mesma rota
        if not all(ponto.get('id_rota') == id_rota for ponto in pontos):
            return Response(
                {"success": False, "detail": "Todos os pontos devem pertencer à mesma rota."},
                status=status.HTTP_400_BAD_REQUEST
            )

        pontos_processados = []
        ids_processados = set()

        # Processa cada ponto na ordem da lista
        for ordem, ponto_data in enumerate(pontos, start=1):
            try:
                dados_ponto = {
                    'ordem': ordem,
                    'latitude': ponto_data['latitude'],
                    'longitude': ponto_data['longitude'],
                    'id_rota': rota
                }

                ponto_id = ponto_data.get('id')

                if ponto_id:
                    try:
                        # Tenta encontrar o ponto existente
                        ponto = PontoTrajeto.objects.get(
                            id=ponto_id, id_rota=rota)
                        # Atualiza os campos
                        for key, value in dados_ponto.items():
                            setattr(ponto, key, value)
                        ponto.save()
                    except PontoTrajeto.DoesNotExist:
                        # Se o ponto não existe, cria um novo
                        ponto = PontoTrajeto.objects.create(**dados_ponto)
                else:
                    ponto = PontoTrajeto.objects.create(**dados_ponto)

                pontos_processados.append({
                    'id': ponto.id,
                    'ordem': ponto.ordem,
                    'latitude': str(ponto.latitude),
                    'longitude': str(ponto.longitude),
                    'id_rota': ponto.id_rota.id
                })

                # Adiciona o ID ao conjunto
                ids_processados.add(ponto.id)

            except KeyError as e:
                return Response(
                    {"success": False,
                        "detail": f"Campo obrigatório ausente: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Remove pontos que não foram incluídos na lista
        PontoTrajeto.objects.filter(id_rota=rota).exclude(
            id__in=ids_processados).delete()

        # Prepara e executa o logging após todas as operações terem sido concluídas com sucesso
        if pontos_processados:
            log_data = {
                'pontos_atualizados': len(pontos_processados),
                'rota_id': id_rota,
                'rota_nome': str(rota),
                'before': pontos_anteriores,
                'after': pontos_processados
            }

            # Obtém o primeiro ponto para o log
            primeiro_ponto = PontoTrajeto.objects.filter(
                id__in=ids_processados, id_rota=rota
            ).order_by('ordem').first()

            if primeiro_ponto:
                self.perform_log_action(
                    instance=primeiro_ponto,
                    action_flag=6,  # BULK_UPDATE
                    log_data=log_data
                )

        return Response({
            "success": True,
            "detail": "Pontos atualizados com sucesso.",
            "pontos": pontos_processados
        }, status=status.HTTP_200_OK)


class PontoOnibusViewSet(LoggableMixin, viewsets.ModelViewSet):
    queryset = PontoOnibus.objects.all()
    serializer_class = PontoOnibusSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'pontos_por_rota_nome']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], url_path='rota-nome/(?P<rota_nome>[^/]+)')
    def pontos_por_rota_nome(self, request, rota_nome=None):
        rota_principal, rotas_variacoes, erro = obter_rota_principal_e_variacoes(
            rota_nome)
        if erro:
            return Response(erro, status=400)

        rotas_relacionadas = [rota_principal] + list(rotas_variacoes)
        pontos_por_variacao = {}

        for rota in rotas_relacionadas:
            pontos_ordenados = PontoOnibus.objects.filter(
                rotapontoonibus__id_rota=rota
            ).order_by('rotapontoonibus__ordem')

            pontos_serializados = PontoOnibusSerializer(
                pontos_ordenados, many=True).data

            nome_variacao = rota.nome_variacao if rota.nome_variacao else "principal"

            if nome_variacao not in pontos_por_variacao:
                nome_variacao = normalize_route_name(nome_variacao)
                pontos_por_variacao[nome_variacao] = []

            pontos_por_variacao[nome_variacao].extend(pontos_serializados)

        return Response(pontos_por_variacao, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            pontos_onibus = PontoOnibus.objects.get(pk=self.kwargs["pk"])
        except PontoOnibus.DoesNotExist:
            return Response({
                "success": False,
                "message": "O ponto de ônibus solicitado não foi encontrado."
            }, status=status.HTTP_404_NOT_FOUND)
        super().destroy(request, *args, **kwargs)
        return Response({
            "success": True,
            "message": "Ponto de ônibus desativado com sucesso."
        }, status=status.HTTP_200_OK)


class RotaPontoOnibusViewSet(LoggableMixin, viewsets.ModelViewSet):
    queryset = RotaPontoOnibus.objects.all()
    serializer_class = RotaPontoOnibusSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'filtrar']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        id_rota = request.data.get('rota_id')
        if not id_rota:
            return Response(
                {"sucess": False, "detail": "O campo 'rota_id' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )

        ultima_ordem = RotaPontoOnibus.objects.filter(
            id_rota=id_rota).order_by('-ordem').first()
        nova_ordem = (ultima_ordem.ordem + 1) if ultima_ordem else 1
        data = request.data.copy()
        data['ordem'] = nova_ordem
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='filtrar', url_name='filtrar')
    def filtrar(self, request):
        id_rota = request.data.get('rota_id')
        id_ponto_onibus = request.data.get('ponto_onibus_id')

        if not id_rota and not id_ponto_onibus:
            return Response(
                {"detail": "É necessário fornecer ao menos 'id_rota' ou 'id_ponto_onibus'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.queryset
        if id_rota:
            queryset = queryset.filter(id_rota=id_rota)
        if id_ponto_onibus:
            queryset = queryset.filter(id_ponto_onibus=id_ponto_onibus)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationViewSet(LoggableMixin, viewsets.ModelViewSet):
    queryset = Notification.objects.filter(read=False)
    serializer_class = NotificationSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['post'], url_path='send')
    def send_notification(self, request, pk=None):
        try:
            notification = Notification.objects.get(pk=pk)
        except Notification.DoesNotExist:
            return Response({
                "success": False,
                "message": "A notificação solicitada não foi encontrada"
            }, status=status.HTTP_404_NOT_FOUND)

        title = notification.title
        body = notification.message
        click_action = "https://dev.garopabus.uk/user/ajuda/" if TYPE_ENV == "development" else "https://garopabus.uk/user/ajuda/"

        if not all([title, body, click_action]):
            return Response({
                "success": False,
                "message": "A notificação não possui todos os dados necessários para ser enviada."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            count_success = send_push_notification(
                title=title,
                body=body,
                click_action=click_action
            )

            log_data = {
                'notification_id': notification.pk,
                'title': title,
                'body': body,
                'count_success': count_success,
                'click_action': click_action,
            }

            self.perform_log_action(
                instance=notification,
                action_flag=4,  # SEND_NOTIFICATION
                log_data=log_data
            )

            return Response({
                "success": True,
                "detail": f"Notificação enviada com sucesso, para {count_success} usuários."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"detail": f"Erro ao enviar notificação: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = Notification.objects.get(pk=self.kwargs["pk"])
        except Notification.DoesNotExist:
            return Response({
                "success": False,
                "message": "A notificação solicitada não foi encontrada"
            }, status=status.HTTP_404_NOT_FOUND)

        if instance.read:
            return Response({
                "success": False,
                "message": "A notificação já está lida"
            }, status=status.HTTP_400_BAD_REQUEST)
        instance.read = True
        instance.save()
        self.perform_log_action(
            instance,
            action_flag=DELETION,
            log_data={
                "changes": [
                    {"field": "read", "from": False, "to": True}
                ]
            }
        )
        return Response({
            "success": True,
            "message": "Notificação marcada como lida com sucesso"
        }, status=status.HTTP_200_OK)


class PushSubscriptionViewSet(LoggableMixin, viewsets.ModelViewSet):
    queryset = PushSubscription.objects.all()
    serializer_class = PushSubscriptionSerializer

    def get_permissions(self):
        if self.action in ['create', 'get_vapid_public_key']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = PushSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Endpoint cadastrado com sucesso."
            }, status=status.HTTP_201_CREATED)
        if "endpoint" in serializer.errors:
            return Response({
                "success": False,
                "message": "Este Endpoint já está cadastrado."
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='vapid-key')
    def get_vapid_public_key(self, request):
        return Response({
            "vapid_public_key": VAPID_PUBLIC_KEY
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def validate_token(request):
    return Response({'message': 'Token válido!'}, status=200)
