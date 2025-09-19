from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from core.models import Venda
from core.serializers.venda import VendaSerializer

class VendaViewSet(ModelViewSet):
    queryset = Venda.objects.all().order_by('-data_venda')
    serializer_class = VendaSerializer
    
    def get_queryset(self):
        """Filtra vendas por data se fornecido."""
        queryset = super().get_queryset()
        data_inicio = self.request.query_params.get('data_inicio')
        data_fim = self.request.query_params.get('data_fim')
        
        if data_inicio:
            queryset = queryset.filter(data_venda__date__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_venda__date__lte=data_fim)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def relatorio_vendas(self, request):
        """Gera relatório de vendas por período."""
        hoje = timezone.now().date()
        ontem = hoje - timedelta(days=1)
        semana = hoje - timedelta(days=7)
        mes = hoje - timedelta(days=30)
        
        vendas_hoje = self.queryset.filter(data_venda__date=hoje, status='finalizada')
        vendas_ontem = self.queryset.filter(data_venda__date=ontem, status='finalizada')
        vendas_semana = self.queryset.filter(data_venda__date__gte=semana, status='finalizada')
        vendas_mes = self.queryset.filter(data_venda__date__gte=mes, status='finalizada')
        
        return Response({
            'hoje': {
                'total': vendas_hoje.aggregate(Sum('total'))['total__sum'] or 0,
                'quantidade': vendas_hoje.count()
            },
            'ontem': {
                'total': vendas_ontem.aggregate(Sum('total'))['total__sum'] or 0,
                'quantidade': vendas_ontem.count()
            },
            'semana': {
                'total': vendas_semana.aggregate(Sum('total'))['total__sum'] or 0,
                'quantidade': vendas_semana.count()
            },
            'mes': {
                'total': vendas_mes.aggregate(Sum('total'))['total__sum'] or 0,
                'quantidade': vendas_mes.count()
            }
        })