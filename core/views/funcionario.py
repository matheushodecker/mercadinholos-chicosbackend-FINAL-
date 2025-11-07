from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.models import Funcionario
from core.serializers.funcionario import FuncionarioSerializer

# --- NOVO --- Importe o 'action' e 'Response'
from rest_framework.decorators import action
from rest_framework.response import Response

class FuncionarioViewSet(ModelViewSet):
    serializer_class = FuncionarioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['cargo', 'ativo']
    search_fields = ['nome', 'email', 'telefone']
    ordering_fields = ['nome', 'data_admissao', 'salario']

    def get_queryset(self):
        """Optimize queries with select_related to avoid N+1 queries."""
        # A ordenação padrão já será 'nome'
        return Funcionario.objects.select_related('cargo').order_by('nome')

    # --- NOVA FUNÇÃO ---
    # Esta action cria o endpoint: /api/funcionarios/todos/
    @action(detail=False, methods=['get'])
    def todos(self, request):
        """
        Retorna todos os funcionários ATIVOS sem paginação
        para uso em dropdowns no frontend.
        """
        # Filtramos por 'ativo=True' (ideal para dropdowns)
        # e usamos a mesma otimização do get_queryset
        queryset = Funcionario.objects.select_related('cargo') \
                                      .filter(ativo=True) \
                                      .order_by('nome')
        
        # Serializa os dados
        serializer = self.get_serializer(queryset, many=True)
        
        # Retorna a resposta
        return Response(serializer.data)