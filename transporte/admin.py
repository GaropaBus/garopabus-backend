from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
import json
from django.utils.safestring import mark_safe
from django.template.defaultfilters import date as date_filter


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time_formatted', 'user_info',
                    'action_type', 'resource_info', 'get_details')
    list_filter = ('action_flag', 'user', 'content_type')
    search_fields = ('object_repr', 'change_message', 'user__username')
    date_hierarchy = 'action_time'
    readonly_fields = ('action_time', 'user', 'content_type',
                       'object_id', 'object_repr', 'action_flag', 'change_message')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def action_time_formatted(self, obj):
        return date_filter(obj.action_time, "d/m/Y H:i:s")
    action_time_formatted.short_description = 'Data/Hora'

    def user_info(self, obj):
        try:
            log_data = json.loads(obj.change_message)
            ip = log_data['request']['user'].get('ip', 'N/A')
            email = log_data['request']['user'].get('email', 'N/A')
            return format_html(
                '<div style="min-width:200px">'
                '<strong>{}</strong><br>'
                '<small>IP: {}<br>Email: {}</small>'
                '</div>',
                obj.user.username,
                ip,
                email
            )
        except:
            return obj.user.username
    user_info.short_description = 'Usuário'

    def action_type(self, obj):
        action_types = {
            1: 'Adição',
            2: 'Alteração',
            3: 'Exclusão',
            4: 'Notificação',
            5: 'Login',
            6: 'Atualização em Massa'  # Novo tipo
        }
        try:
            log_data = json.loads(obj.change_message)
            action = log_data['action']['type']
            color_map = {
                'created': 'success',
                'updated': 'warning',
                'deleted': 'danger',
                'send_notification': 'info',
                'jwt_login': 'primary',
                'bulk_update': 'darkOrange'
            }
            color = color_map.get(action, 'secondary')
            return format_html(
                '<span class="badge badge-{}" style="padding:5px 10px; '
                'border-radius:3px; background-color:{};">{}</span>',
                color,
                {
                    'success': '#28a745',
                    'warning': '#ffc107',
                    'danger': '#dc3545',
                    'info': '#17a2b8',
                    'primary': '#007bff',
                    'secondary': '#6c757d',
                    'darkOrange': '#ff8c00'
                }[color],
                action.upper()
            )
        except:
            return action_types.get(obj.action_flag, 'Desconhecido')

    def resource_info(self, obj):
        try:
            log_data = json.loads(obj.change_message)
            resource = log_data['resource']
            return format_html(
                '<div style="min-width:150px">'
                '<strong>{}</strong><br>'
                '<small>Tipo: {}<br>ID: {}</small>'
                '</div>',
                resource['str_representation'],
                resource['type'],
                resource['id']
            )
        except:
            return obj.object_repr
    resource_info.short_description = 'Recurso'

    def get_details(self, obj):
        try:
            log_data = json.loads(obj.change_message)
            details = log_data['action']['details']

            # Bulk Update
            if log_data['action']['type'] == 'bulk_update':
                return format_html(
                    '<div style="min-width:200px">'
                    '<strong>Pontos Atualizados:</strong> {}<br>'
                    '</div>',
                    details['pontos_atualizados'],
                )

            # Login
            if log_data['action']['type'] == 'jwt_login':
                return format_html(
                    '<div style="min-width:200px">'
                    '<strong>Login via {}</strong><br>'
                    '<small>Status: {}</small>'
                    '</div>',
                    details['login_type'].upper(),
                    details['status']
                )

            # Update
            elif 'changes' in details:
                changes_html = [
                    '<div style="margin-bottom:5px;"><strong>Alterações:</strong></div>']
                for change in details['changes']:
                    changes_html.append(
                        f'<div style="margin-left:10px;margin-bottom:3px;">'
                        f'<strong>{change["field"]}:</strong> '
                        f'<span style="color:#dc3545">{str(change["from"]) or "vazio"}</span> → '
                        f'<span style="color:#28a745">{str(change["to"]) or "vazio"}</span>'
                        f'</div>'
                    )
                return mark_safe(''.join(changes_html))

            # Create
            elif 'created_data' in details:
                data = details['created_data']
                html = ['<div><strong>Dados criados:</strong></div>']
                for key, value in data.items():
                    if key != 'id':
                        html.append(
                            f'<div style="margin-left:10px;">'
                            f'<strong>{key}:</strong> {value}'
                            f'</div>'
                        )
                return mark_safe(''.join(html))

            # Delete
            elif 'deleted_data' in details:
                data = details['deleted_data']
                html = ['<div><strong>Dados excluídos:</strong></div>']
                for key, value in data.items():
                    if key != 'id':
                        html.append(
                            f'<div style="margin-left:10px;">'
                            f'<strong>{key}:</strong> {value}'
                            f'</div>'
                        )
                return mark_safe(''.join(html))

            # Notification
            elif 'notification_id' in details:
                return format_html(
                    '<div>'
                    '<strong>Título:</strong> {}<br>'
                    '<strong>Mensagem:</strong> {}<br>'
                    '<strong>Usuarios que receberam:</strong> {}<br>'
                    '<strong>Link:</strong> <a href="{}" target="_blank">Abrir</a>'
                    '</div>',
                    details['title'],
                    details['body'],
                    details['count_success'],
                    details.get('click_action', '#')
                )

            return str(details)
        except:
            return 'N/A'
    get_details.short_description = 'Detalhes'

    class Media:
        css = {
            'all': ('admin/css/log_entry.css',)
        }
