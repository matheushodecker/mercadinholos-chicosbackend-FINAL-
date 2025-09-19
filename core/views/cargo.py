from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.models import Cargo
from core.serializers.cargo import CargoSerializer

class CargoViewSet(ModelViewSet):
    queryset = Cargo.objects.all().order_by('nome')
    serializer_class = CargoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'salario_base', 'data_criacao']
