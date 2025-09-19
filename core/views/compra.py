from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.models import Compra, ItemCompra
from core.serializers.compra import CompraSerializer

class CompraViewSet(ModelViewSet):
    serializer_class = CompraSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Campo de filtro alterado de 'usuario' para 'funcionario'
    filterset_fields = ['status', 'fornecedor', 'funcionario']
    search_fields = ['numero_pedido', 'observacoes']
    ordering_fields = ['data_pedido', 'valor_total', 'data_entrega_prevista']

    def get_queryset(self):
        """Optimize queries with select_related and prefetch_related to avoid N+1 queries."""
        # 'select_related' alterado de 'usuario' para 'funcionario'
        return Compra.objects.select_related('fornecedor', 'funcionario').prefetch_related(
            Prefetch('itens', queryset=ItemCompra.objects.select_related('produto'))
        ).order_by('-data_pedido')