from rest_framework import serializers
from .models import Rota, HorarioOnibus, PontoTrajeto, PontoOnibus, RotaPontoOnibus, Notification, PushSubscription

class RotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rota
        fields = '__all__'

class HorarioOnibusSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioOnibus
        fields = '__all__'

class PontoTrajetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PontoTrajeto
        fields = '__all__'

class PontoOnibusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PontoOnibus
        fields = '__all__'

class RotaPontoOnibusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RotaPontoOnibus
        fields = '__all__'
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        
class PushSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushSubscription
        fields = ['endpoint', 'public_key', 'auth_key']