from rest_framework.serializers import ModelSerializer, SerializerMethodField
from core.models import Estoque, MovimentacaoEstoque

class EstoqueSerializer(ModelSerializer):
    produto_nome = SerializerMethodField()
    estoque_baixo = SerializerMethodField()
    estoque_alto = SerializerMethodField()
    
    class Meta:
        model = Estoque
        fields = [
            'id', 'produto', 'produto_nome', 'quantidade_atual',
            'quantidade_minima', 'quantidade_maxima', 'localizacao',
            'estoque_baixo', 'estoque_alto', 'data_ultima_movimentacao'
        ]
        read_only_fields = ['id', 'data_ultima_movimentacao', 'estoque_baixo', 'estoque_alto']

    def get_produto_nome(self, obj):
        """Get product name."""
        return obj.produto.nome if obj.produto else None

    def get_estoque_baixo(self, obj):
        """Check if stock is low."""
        return obj.estoque_baixo

    def get_estoque_alto(self, obj):
        """Check if stock is high."""
        return obj.estoque_alto

class MovimentacaoEstoqueSerializer(ModelSerializer):
    produto_nome = SerializerMethodField()
    # Campo do serializer renomeado
    funcionario_nome = SerializerMethodField()
    tipo_movimentacao_display = SerializerMethodField()
    
    class Meta:
        model = MovimentacaoEstoque
        fields = [
            'id', 'produto', 'produto_nome', 'tipo_movimentacao',
            'tipo_movimentacao_display', 'quantidade', 'quantidade_anterior',
            'quantidade_atual', 'motivo', 'funcionario', 'funcionario_nome',
            'data_movimentacao', 'observacoes'
        ]
        read_only_fields = ['id', 'data_movimentacao']

    def get_produto_nome(self, obj):
        """Get product name."""
        return obj.produto.nome if obj.produto else None

    def get_funcionario_nome(self, obj):
        """Get user name."""
        # Acesso ao objeto renomeado
        return obj.funcionario.nome if obj.funcionario else None

    def get_tipo_movimentacao_display(self, obj):
        """Get movement type display name."""
        return obj.get_tipo_movimentacao_display()