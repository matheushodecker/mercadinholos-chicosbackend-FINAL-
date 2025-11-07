from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.models import Categoria
from core.serializers.categoria import CategoriaSerializer

# --- NOVO --- Importe o 'action' e 'Response'
from rest_framework.decorators import action
from rest_framework.response import Response

class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all().order_by('nome')
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'data_criacao']

    # --- NOVA FUNÇÃO ---
    # Esta action cria o endpoint: /api/categorias/todos/
    @action(detail=False, methods=['get'])
    def todos(self, request):
        """
        Retorna todas as categorias ATIVAS sem paginação
        para uso em dropdowns no frontend.
        """
        # Filtramos por 'ativo=True' pois não faz sentido 
        # selecionar uma categoria inativa em um novo produto.
        queryset = Categoria.objects.filter(ativo=True).order_by('nome')
        
        # Serializa os dados (usando o serializer da classe)
        serializer = self.get_serializer(queryset, many=True)
        
        # Retorna a resposta
        return Response(serializer.data)