from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.models import FormaPagamento, Pagamento
from core.serializers.pagamento import FormaPagamentoSerializer, PagamentoSerializer

class FormaPagamentoViewSet(ModelViewSet):
    queryset = FormaPagamento.objects.all().order_by('nome')
    serializer_class = FormaPagamentoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'taxa_percentual', 'taxa_fixa']

class PagamentoViewSet(ModelViewSet):
    serializer_class = PagamentoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'forma_pagamento', 'venda']
    search_fields = ['observacoes']
    # 'data_pagamento' foi substituído por 'data_vencimento' e 'data_recebimento'
    ordering_fields = ['data_vencimento', 'data_recebimento', 'valor']

    def get_queryset(self):
        """Optimize queries with select_related to avoid N+1 queries."""
        # 'data_pagamento' foi substituído por 'data_vencimento'
        return Pagamento.objects.select_related('venda', 'forma_pagamento').order_by('-data_vencimento')