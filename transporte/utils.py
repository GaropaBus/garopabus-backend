import json
from pywebpush import webpush, WebPushException
from .models import PushSubscription
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