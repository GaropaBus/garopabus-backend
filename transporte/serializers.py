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
    # Renomeando `id_rota` para `rota`
    rota = RotaSerializer(read_only=True, source="id_rota")
    rota_id = serializers.PrimaryKeyRelatedField(
        queryset=Rota.objects.all(), source="id_rota", write_only=True
    )  # Para input

    # Renomeando `id_ponto_onibus` para `ponto_onibus`
    ponto_onibus = PontoOnibusSerializer(
        read_only=True, source="id_ponto_onibus")
    ponto_onibus_id = serializers.PrimaryKeyRelatedField(
        queryset=PontoOnibus.objects.all(), source="id_ponto_onibus", write_only=True
    )

    class Meta:
        model = RotaPontoOnibus
        fields = ["id", "rota", "rota_id",
                  "ponto_onibus", "ponto_onibus_id", "ordem"]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class PushSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushSubscription
        fields = ['endpoint', 'public_key', 'auth_key']
