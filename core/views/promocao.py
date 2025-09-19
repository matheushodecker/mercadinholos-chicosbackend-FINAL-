from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.models import Promocao, ProdutoPromocao
from core.serializers.promocao import PromocaoSerializer

class PromocaoViewSet(ModelViewSet):
    serializer_class = PromocaoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['ativo', 'tipo_desconto']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'data_inicio', 'data_fim']

    def get_queryset(self):
        """Optimize queries with prefetch_related to avoid N+1 queries."""
        return Promocao.objects.prefetch_related(
            Prefetch('produtos', queryset=ProdutoPromocao.objects.select_related('produto'))
        ).order_by('-data_inicio')
    
    @action(detail=False, methods=['get'])
    def promocoes_ativas(self, request):
        """Retorna promoções ativas no momento."""
        agora = timezone.now()
        promocoes = self.get_queryset().filter(
            ativo=True,
            data_inicio__lte=agora,
            data_fim__gte=agora
        )
        serializer = self.get_serializer(promocoes, many=True)
        return Response(serializer.data)
