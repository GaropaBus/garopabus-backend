from django.db import models

# Create your models here.

# Enum para os tipos de dia da semana
class TipoDiaSemana(models.TextChoices):
    DIA_UTIL = 'dia_util'
    FINAL_SEMANA_FERIADO = 'final_semana_feriado'

# Modelo para a tabela de "rotas"
class Rota(models.Model):
    bairro_origem = models.CharField(max_length=100)
    bairro_destino  = models.CharField(max_length=100)
    nome_variacao = models.CharField(max_length=100, null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=[('principal', 'Principal'), ('variacao', 'Variação')])
    id_rota_principal = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.bairro_origem } - { self.bairro_destino }'

# Modelo para a tabela de "horarios_onibus"
class HorarioOnibus(models.Model):
    id_rota = models.ForeignKey(Rota, on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=20, choices=TipoDiaSemana.choices)
    hora_partida = models.TimeField()
    hora_chegada = models.TimeField()

    def __str__(self):
        return f'{self.id_rota.bairro_origem } - { self.id_rota.bairro_destino } / {self.dia_semana}'

# Modelo para a tabela de "pontos_trajeto"
class PontoTrajeto(models.Model):
    id_rota = models.ForeignKey(Rota, on_delete=models.CASCADE)
    ordem = models.IntegerField()
    latitude = models.DecimalField(max_digits=18, decimal_places=14)
    longitude = models.DecimalField(max_digits=18, decimal_places=14)

    def __str__(self):
        return f'Ponto {self.id} - {self.id_rota.nome}'

# Modelo para a tabela de "pontos_onibus"
class PontoOnibus(models.Model):
    latitude = models.DecimalField(max_digits=18, decimal_places=14)
    longitude = models.DecimalField(max_digits=18, decimal_places=14)
    link_maps = models.TextField()

    def __str__(self):
        return f'Ponto {self.id} - Latitude: {self.latitude}, Longitude: {self.longitude}'

# Modelo para a tabela de "rotas_ponto_onibus"
class RotaPontoOnibus(models.Model):
    id_rota = models.ForeignKey(Rota, on_delete=models.CASCADE)
    id_ponto_onibus = models.ForeignKey(PontoOnibus, on_delete=models.CASCADE)
    ordem = models.IntegerField()

    def __str__(self):
        return f'Rota {self.id_rota.nome} - Ponto {self.id_ponto_onibus.id}'
