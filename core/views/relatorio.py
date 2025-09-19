from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
# Importa o modelo de Estoque para poder realizar os cálculos
from core.models import RelatorioVenda, RelatorioEstoque, Estoque
from core.serializers.relatorio import RelatorioVendaSerializer, RelatorioEstoqueSerializer
from django.db.models import Sum, F

class RelatorioVendaViewSet(ModelViewSet):
    serializer_class = RelatorioVendaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['funcionario_gerador']
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['data_geracao', 'total_vendas']

    def get_queryset(self):
        return RelatorioVenda.objects.select_related('funcionario_gerador').order_by('-data_geracao')

class RelatorioEstoqueViewSet(ModelViewSet):
    serializer_class = RelatorioEstoqueSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['funcionario_gerador']
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['data_geracao', 'produtos_baixo_estoque']

    def get_queryset(self):
        return RelatorioEstoque.objects.select_related(
            'funcionario_gerador'
        ).order_by('-data_geracao')

    def create(self, request, *args, **kwargs):
        # Valida os dados da requisição usando o serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 1. Calcule os valores para o relatório
        # Total de produtos (assumindo que você tem um modelo Estoque)
        total_produtos = Estoque.objects.aggregate(total=Sum('quantidade_atual'))['total'] or 0
        
        # Produtos com estoque baixo
        produtos_baixo_estoque = Estoque.objects.filter(quantidade_atual__lte=F('quantidade_minima')).count()
        
        # Valor total do estoque
        # **Ajuste o campo 'preco' para o nome do campo de preço no seu modelo Produto**
        valor_total_estoque = Estoque.objects.aggregate(
            total=Sum(F('quantidade_atual') * F('produto__preco_venda'))
        )['total'] or 0

        # 2. Adicione os valores calculados aos dados validados
        validated_data = serializer.validated_data
        validated_data['total_produtos'] = total_produtos
        validated_data['produtos_estoque_baixo'] = produtos_baixo_estoque
        validated_data['valor_total_estoque'] = valor_total_estoque
        
        # 3. Crie e salve a instância do relatório com todos os dados
        instance = serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)