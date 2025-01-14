from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from django.utils import timezone
import json


SEND_NOTIFICATION = 4
LOGIN_ACTION = 5
BULK_UPDATE = 6


class LoggableMixin:
    """
    Mixin para logging detalhado de operações na API.
    Registra informações sobre quem fez a ação, o que foi feito e quando.
    """

    def get_client_ip(self):
        """Obtém o IP do cliente da requisição."""
        request = self.request
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_request_info(self):
        """Coleta informações básicas da requisição."""
        request = self.request
        return {
            'endpoint': request.path,
            'method': request.method,
            'timestamp': timezone.now().isoformat(),
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'ip': self.get_client_ip()
            }
        }

    def perform_log_action(self, instance, action_flag, log_data):
        """Registra a ação no sistema de logs."""
        if not self.request.user.is_authenticated:
            return

        # Estrutura base do log
        log_entry = {
            'request': self.get_request_info(),
            'action': {
                'type': self.get_action_type(action_flag),
                'details': log_data
            },
            'resource': {
                'id': instance.id,
                'type': instance._meta.model_name,
                'str_representation': str(instance)
            }
        }

        # Usando change_message como o JSON estruturado
        LogEntry.objects.log_action(
            user_id=self.request.user.id,
            content_type_id=ContentType.objects.get_for_model(instance).id,
            object_id=instance.id,
            object_repr=str(instance),
            action_flag=action_flag,
            change_message=json.dumps(log_entry, default=str)
        )

    def get_action_type(self, action_flag):
        """Converte action_flag para string legível."""
        return {
            ADDITION: 'created',
            CHANGE: 'updated',
            DELETION: 'deleted',
            SEND_NOTIFICATION: 'send_notification',
            LOGIN_ACTION: 'jwt_login',
            BULK_UPDATE: 'bulk_update'
        }.get(action_flag, 'unknown')

    def create(self, request, *args, **kwargs):
        """Log de criação de recurso."""
        response = super().create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            instance = self.get_queryset().get(id=response.data['id'])

            log_data = {
                'created_data': response.data,
                'request_payload': request.data
            }

            self.perform_log_action(
                instance=instance,
                action_flag=ADDITION,
                log_data=log_data
            )

        return response

    def update(self, request, *args, **kwargs):
        """Log de atualização de recurso."""
        instance = self.get_object()
        old_data = self.get_instance_data(instance)

        response = super().update(request, *args, **kwargs)

        if response.status_code in [status.HTTP_200_OK, status.HTTP_202_ACCEPTED]:
            updated_instance = self.get_object()
            new_data = self.get_instance_data(updated_instance)

            changes = self.get_changes(old_data, new_data)
            if changes:
                log_data = {
                    'changes': changes,
                    'request_payload': request.data
                }

                self.perform_log_action(
                    instance=updated_instance,
                    action_flag=CHANGE,
                    log_data=log_data
                )

        return response

    def destroy(self, request, *args, **kwargs):
        """Sobrescreve destroy com logging aprimorado."""
        instance = self.get_object()
        instance_data = self.get_instance_data(instance)

        detailed_message = {
            'deleted_data': instance_data,
        }
        self.perform_log_action(
            instance=instance,
            action_flag=DELETION,
            log_data=detailed_message
        )
        return super().destroy(request, *args, **kwargs)

    def get_instance_data(self, instance):
        """Obtém dados relevantes da instância."""
        data = {}
        for field in instance._meta.fields:
            value = getattr(instance, field.name)
            # Para campos relacionais, usa str() para evitar problemas de serialização
            if hasattr(value, '_meta'):
                data[field.name] = str(value)
            else:
                data[field.name] = value
        return data

    def get_changes(self, old_data, new_data):
        """Identifica mudanças entre estados."""
        changes = []

        for key in old_data.keys():
            if key in new_data and old_data[key] != new_data[key]:
                changes.append({
                    'field': key,
                    'from': old_data[key],
                    'to': new_data[key]
                })

        return changes


class LoggingTokenObtainPairView(LoggableMixin, TokenObtainPairView):
    """
    View personalizada para logging de autenticação JWT.
    Herda do LoggableMixin para reaproveitar os métodos de logging.
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Obtém o usuário baseado no username fornecido
            username = request.data.get('username')
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(username=username)

            log_data = {
                'login_type': 'jwt',
                'status': 'success',
                'request_data': {
                    'username': username,
                }
            }

            self.request = request
            self.request.user = user

            self.perform_log_action(
                instance=user,
                action_flag=LOGIN_ACTION,
                log_data=log_data
            )

        return response


@receiver(user_logged_in)
def log_admin_login(sender, request, user, **kwargs):
    """Signal para capturar logins no admin do Django."""
    if request and 'admin' in request.path:
        logger = type('AdminLogger', (LoggableMixin,), {})()
        logger.request = request
        logger.request.user = user

        log_data = {
            'login_type': 'admin',
            'status': 'success',
            'path': request.path
        }

        logger.perform_log_action(
            instance=user,
            action_flag=LOGIN_ACTION,
            log_data=log_data
        )
