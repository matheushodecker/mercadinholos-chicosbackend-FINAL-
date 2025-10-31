from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from core.models import Fornecedor
from core.serializers.fornecedor import FornecedorSerializer


class FornecedorViewSet(ModelViewSet):
    serializer_class = FornecedorSerializer
    permission_classes = [IsAuthenticated]
    
    # --- Filtros, Busca e Ordenação ---
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # (Assumindo que você tenha estes campos para filtrar)
    filterset_fields = ['ativo', 'cidade', 'estado'] 
    search_fields = ['nome', 'nome_fantasia', 'cnpj', 'email', 'telefone']
    ordering_fields = ['nome', 'nome_fantasia', 'data_criacao']

    def get_queryset(self):
        """
        Sobrescreve o queryset base para otimizar
        e retornar apenas fornecedores ativos por padrão.
        """
        # Se seu modelo Fornecedor não tiver o campo 'ativo', 
        # remova o .filter(ativo=True)
        return Fornecedor.objects.filter(ativo=True)

    @action(detail=False, methods=['get'])
    def todos(self, request):
        """
        Retorna TODOS os fornecedores ativos, sem paginação,
        para uso em dropdowns (ex: na tela de Compras ou Produtos).
        """
        # Reutiliza o get_queryset() (que já filtra por ativo=True)
        # e aplica os filtros de busca/ordenação (ex: ?search=...)
        queryset = self.filter_queryset(self.get_queryset())
        
        # Serializa os dados sem paginação
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)