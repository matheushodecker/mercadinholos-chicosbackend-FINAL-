from rest_framework.serializers import ModelSerializer, SerializerMethodField
from core.models import Promocao, ProdutoPromocao

class ProdutoPromocaoSerializer(ModelSerializer):
    produto_nome = SerializerMethodField()
    
    class Meta:
        model = ProdutoPromocao
        fields = [
            'id', 'produto', 'produto_nome',
            'preco_promocional'
        ]
        read_only_fields = ['id']

    def get_produto_nome(self, obj):
        """Get product name."""
        return obj.produto.nome if obj.produto else None

class PromocaoSerializer(ModelSerializer):
    produtos = ProdutoPromocaoSerializer(many=True, required=False)
    tipo_desconto_display = SerializerMethodField()
    promocao_ativa = SerializerMethodField()
    
    class Meta:
        model = Promocao
        fields = [
            'id', 'nome', 'descricao', 'tipo_desconto', 'tipo_desconto_display',
            'valor_desconto', 'data_inicio', 'data_fim',
            'promocao_ativa', 'ativo', 'produtos', 'data_criacao'
        ]
        read_only_fields = ['id', 'data_criacao', 'promocao_ativa']
    
    def get_tipo_desconto_display(self, obj):
        """Get discount type display name."""
        return obj.get_tipo_desconto_display()

    def get_promocao_ativa(self, obj):
        """Check if promotion is active."""
        return obj.promocao_ativa

    def create(self, validated_data):
        """Create promotion with products."""
        produtos_data = validated_data.pop('produtos', [])
        promocao = Promocao.objects.create(**validated_data)
        
        for produto_data in produtos_data:
            # O campo 'promocao' é adicionado aqui
            ProdutoPromocao.objects.create(promocao=promocao, **produto_data)
        
        return promocao

    def update(self, instance, validated_data):
        """Update promotion with products."""
        produtos_data = validated_data.pop('produtos', [])
        
        # Update promotion fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update products if provided
        if produtos_data:
            instance.produtos.all().delete()
            for produto_data in produtos_data:
                # O campo 'promocao' é adicionado aqui
                ProdutoPromocao.objects.create(promocao=instance, **produto_data)
        
        instance.save()
        return instance