from rest_framework import serializers
from .models import Rota, HorarioOnibus, PontoTrajeto, PontoOnibus, RotaPontoOnibus

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