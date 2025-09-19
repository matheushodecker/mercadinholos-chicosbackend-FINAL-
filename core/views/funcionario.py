from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.models import Funcionario
from core.serializers.funcionario import FuncionarioSerializer

class FuncionarioViewSet(ModelViewSet):
    serializer_class = FuncionarioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['cargo', 'ativo']
    search_fields = ['nome', 'email', 'telefone']
    ordering_fields = ['nome', 'data_admissao', 'salario']

    def get_queryset(self):
        """Optimize queries with select_related to avoid N+1 queries."""
        return Funcionario.objects.select_related('cargo').order_by('nome')
