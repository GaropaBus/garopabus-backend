import django_filters
from .models import Rota

class RotaFilter(django_filters.FilterSet):
    bairro_origem = django_filters.CharFilter(field_name="bairro_origem", lookup_expr='icontains')
    bairro_destino = django_filters.CharFilter(field_name="bairro_destino", lookup_expr='icontains')
    tipo = django_filters.ChoiceFilter(field_name="tipo", choices=Rota._meta.get_field("tipo").choices)
    nome_variacao = django_filters.CharFilter(field_name="nome_variacao", lookup_expr='icontains')

    class Meta:
        model = Rota
        fields = ['bairro_origem', 'bairro_destino', 'tipo', 'nome_variacao']
