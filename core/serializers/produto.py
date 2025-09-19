from rest_framework.serializers import ModelSerializer, SerializerMethodField
from core.models import Produto

class ProdutoSerializer(ModelSerializer):
    categoria_nome = SerializerMethodField()
    fornecedor_nome = SerializerMethodField()
    margem_lucro = SerializerMethodField()
    estoque_baixo = SerializerMethodField()

    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'descricao', 'codigo_barras',
            'categoria', 'categoria_nome', 'fornecedor', 'fornecedor_nome',
            'preco_custo', 'preco_venda', 'estoque_atual', 'estoque_minimo',
            'margem_lucro', 'estoque_baixo', 'ativo', 'data_criacao'
        ]
        read_only_fields = ['id', 'data_criacao', 'margem_lucro', 'estoque_baixo']

    def get_categoria_nome(self, obj):
        """Get category name."""
        return obj.categoria.nome if obj.categoria else None

    def get_fornecedor_nome(self, obj):
        """Get supplier name."""
        return obj.fornecedor.nome if obj.fornecedor else None

    def get_margem_lucro(self, obj):
        """Get profit margin."""
        return obj.margem_lucro

    def get_estoque_baixo(self, obj):
        """Check if stock is low."""
        return obj.estoque_baixo
