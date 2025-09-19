from rest_framework.serializers import ModelSerializer, SerializerMethodField
from core.models import FormaPagamento, Pagamento

class FormaPagamentoSerializer(ModelSerializer):
    class Meta:
        model = FormaPagamento
        fields = [
            'id', 'nome', 'descricao', 'taxa_percentual', 'taxa_fixa', 
            'prazo_recebimento', 'ativo', 'data_criacao'
        ]
        read_only_fields = ['id', 'data_criacao']

class PagamentoSerializer(ModelSerializer):
    venda_numero = SerializerMethodField()
    forma_pagamento_nome = SerializerMethodField()
    status_display = SerializerMethodField()
    
    class Meta:
        model = Pagamento
        fields = [
            'id', 'venda', 'venda_numero', 'forma_pagamento',  
            'forma_pagamento_nome', 'valor', 'data_vencimento',
            'data_recebimento', 'status', 'status_display', 'observacoes'
        ]
        read_only_fields = ['id']

    def get_venda_numero(self, obj):
        """Get sale number."""
        return getattr(obj.venda, 'numero_venda', None) if obj.venda else None

    def get_forma_pagamento_nome(self, obj):
        """Get payment method name."""
        return obj.forma_pagamento.nome if obj.forma_pagamento else None

    def get_status_display(self, obj):
        """Get status display name."""
        return obj.get_status_display()