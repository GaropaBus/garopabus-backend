import json
import urllib
import unicodedata
from pywebpush import webpush, WebPushException
from .models import PushSubscription
from .models import Rota
from garopabus.settings import VAPID_PRIVATE_KEY, VAPID_ADMIN_EMAIL


def send_push_notification(title, body, click_action):
    subscriptions = PushSubscription.objects.all()
    count_sucess = 0

    for subscription in subscriptions:
        try:
            payload = {
                "title": title,
                "body": body,
                "icon": "https://dev.garopabus.uk/assets/images/favicon.ico",
                "url": click_action,
            }
            webpush(
                subscription_info={
                    "endpoint": subscription.endpoint,
                    "keys": {
                        "p256dh": subscription.public_key,
                        "auth": subscription.auth_key,
                    },
                },
                data=json.dumps(payload),
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims={
                    "sub": f"mailto:{VAPID_ADMIN_EMAIL}",
                },
            )
            count_sucess += 1
        except WebPushException as e:
            error_message = str(e)
            if "410" in error_message or "404" in error_message:
                subscription.delete()
    return count_sucess


def obter_rota_principal_e_variacoes(rota_nome):
    """
    Obtém a rota principal e suas variações a partir do nome da rota.    
    """
    rota_nome = urllib.parse.unquote(rota_nome).lower()
    partes = rota_nome.split('-x-')

    if len(partes) != 2:
        return None, None, {"success": False, "message": "Formato inválido para a rota. Use origem-x-destino."}

    bairro_origem, bairro_destino = partes
    bairro_origem = normalize_route_name(bairro_origem)
    bairro_destino = normalize_route_name(bairro_destino)

    rotas_principais = Rota.objects.filter(tipo="principal")
    rota_principal = None
    for rota in rotas_principais:
        if normalize_route_name(rota.bairro_origem) == bairro_origem and normalize_route_name(rota.bairro_destino) == bairro_destino:
            rota_principal = rota
            break

    if not rota_principal:
        return None, None, {"success": False, "message": "Rota principal não encontrada"}

    variacoes = Rota.objects.filter(id_rota_principal=rota_principal)
    return rota_principal, variacoes, None


def normalize_route_name(text):
    """
    Normaliza o nome da rota:
    - Remove acentos
    - Converte para minúsculas
    - Substitui barras por espaços
    - Remove espaços extras
    """
    text = ''.join(c for c in unicodedata.normalize('NFKD', text)
                   if not unicodedata.combining(c))
    text = text.replace('/', ' ').replace('-', ' ')
    text = '_'.join(text.split()).lower()

    return text
