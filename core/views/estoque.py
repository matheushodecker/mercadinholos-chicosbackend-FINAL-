from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.models import Estoque, MovimentacaoEstoque
from core.serializers.estoque import EstoqueSerializer, MovimentacaoEstoqueSerializer

class EstoqueViewSet(ModelViewSet):
    serializer_class = EstoqueSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['produto__categoria', 'produto__fornecedor']
    search_fields = ['produto__nome', 'localizacao']
    ordering_fields = ['quantidade_atual', 'data_ultima_movimentacao']

    def get_queryset(self):
        """Optimize queries with select_related to avoid N+1 queries."""
        return Estoque.objects.select_related('produto', 'produto__categoria', 'produto__fornecedor')
    
    @action(detail=False, methods=['get'])
    def estoque_baixo(self, request):
        """Retorna produtos com estoque baixo."""
        estoques = self.get_queryset().filter(quantidade_atual__lte=F('quantidade_minima'))
        serializer = self.get_serializer(estoques, many=True)
        return Response(serializer.data)

class MovimentacaoEstoqueViewSet(ModelViewSet):
    serializer_class = MovimentacaoEstoqueSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Campo de filtro alterado de 'usuario' para 'funcionario'
    filterset_fields = ['tipo_movimentacao', 'produto', 'funcionario']
    search_fields = ['motivo', 'observacoes', 'produto__nome']
    ordering_fields = ['data_movimentacao', 'quantidade']

    def get_queryset(self):
        """Optimize queries with select_related to avoid N+1 queries."""
        # 'select_related' alterado de 'usuario' para 'funcionario'
        return MovimentacaoEstoque.objects.select_related('produto', 'funcionario').order_by('-data_movimentacao')