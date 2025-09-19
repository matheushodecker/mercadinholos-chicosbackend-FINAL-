from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.models import Cliente
from core.serializers.cliente import ClienteSerializer

class ClienteViewSet(ModelViewSet):
    queryset = Cliente.objects.all().order_by('nome')
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['ativo', 'cidade', 'estado']
    search_fields = ['nome', 'email', 'telefone', 'cpf_cnpj'] # Campo corrigido para cpf_cnpj
    ordering_fields = ['nome', 'data_nascimento', 'data_cadastro'] # Campo de ordenação corrigido para data_cadastro