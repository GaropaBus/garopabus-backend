from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from rest_framework import status

class LoggableMixin:
    """Mixin para adicionar logs automáticos de alterações no modelo."""

    def perform_log_action(self, instance, action_flag, change_message):
        """Registra logs no sistema de LogEntry."""
        if self.request.user and self.request.user.is_authenticated:
            LogEntry.objects.log_action(
                user_id=self.request.user.id,
                content_type_id=ContentType.objects.get_for_model(instance).id,
                object_id=instance.id,
                object_repr=str(instance),
                action_flag=action_flag,
                change_message=change_message
            )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            # Obter o objeto recém-criado
            instance = self.get_queryset().get(id=response.data['id'])  # Ou use outro campo
            self.perform_log_action(
                instance=instance,
                action_flag=ADDITION,
                change_message="Criado via API."
            )
        return response

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_instance = instance.__class__.objects.get(id=instance.id)
        response = super().update(request, *args, **kwargs)
        updated_instance = self.get_object()
        changes = self.compare_instance_changes(old_instance, updated_instance)
        if changes:
            change_message = [{"action": "update", "changes": changes}]
            self.perform_log_action(
                updated_instance,
                action_flag=CHANGE,
                change_message=change_message
            )
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_log_action(
            instance=instance,
            action_flag=DELETION,
            change_message="Excluído via API."
        )
        return super().destroy(request, *args, **kwargs)

    def compare_instance_changes(self, old_instance, new_instance):
        changes = []
        for field in old_instance._meta.fields:
            field_name = field.name
            old_value = getattr(old_instance, field_name)
            new_value = getattr(new_instance, field_name)

            # Se houver alteração no valor do campo, registra
            if old_value != new_value:
                changes.append({
                    'field': field_name,
                    'old_value': old_value,
                    'new_value': new_value
                })
        return changes