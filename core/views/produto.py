from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.models import Produto
from core.serializers.produto import ProdutoSerializer

class ProdutoViewSet(ModelViewSet):
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['categoria', 'fornecedor', 'ativo']
    search_fields = ['nome', 'descricao', 'codigo_barras']
    ordering_fields = ['nome', 'preco_venda', 'estoque_atual', 'data_criacao']

    def get_queryset(self):
        """Optimize queries with select_related to avoid N+1 queries."""
        return Produto.objects.select_related('categoria', 'fornecedor').filter(ativo=True)
    
    @action(detail=False, methods=['get'])
    def estoque_baixo(self, request):
        """Retorna produtos com estoque baixo."""
        produtos = self.get_queryset().filter(estoque_atual__lte=F('estoque_minimo'))
        serializer = self.get_serializer(produtos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def buscar_por_codigo(self, request):
        """Busca produto por código de barras."""
        codigo = request.query_params.get('codigo')
        if codigo:
            try:
                produto = self.get_queryset().get(codigo_barras=codigo)
                serializer = self.get_serializer(produto)
                return Response(serializer.data)
            except Produto.DoesNotExist:
                return Response({'error': 'Produto não encontrado'}, status=404)
        return Response({'error': 'Código não informado'}, status=400)
