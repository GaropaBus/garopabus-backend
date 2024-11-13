from rest_framework import viewsets
from .models import Rota, HorarioOnibus, Log, PontoTrajeto, PontoOnibus, RotaPontoOnibus
from .serializers import RotaSerializer, HorarioOnibusSerializer, LogSerializer, PontoTrajetoSerializer, PontoOnibusSerializer, RotaPontoOnibusSerializer

class RotaViewSet(viewsets.ModelViewSet):
    queryset = Rota.objects.all()
    serializer_class = RotaSerializer

class HorarioOnibusViewSet(viewsets.ModelViewSet):
    queryset = HorarioOnibus.objects.all()
    serializer_class = HorarioOnibusSerializer

class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer

class PontoTrajetoViewSet(viewsets.ModelViewSet):
    queryset = PontoTrajeto.objects.all()
    serializer_class = PontoTrajetoSerializer

class PontoOnibusViewSet(viewsets.ModelViewSet):
    queryset = PontoOnibus.objects.all()
    serializer_class = PontoOnibusSerializer

class RotaPontoOnibusViewSet(viewsets.ModelViewSet):
    queryset = RotaPontoOnibus.objects.all()
    serializer_class = RotaPontoOnibusSerializer
