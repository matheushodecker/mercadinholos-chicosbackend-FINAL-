from rest_framework.serializers import ModelSerializer, SerializerMethodField
from core.models import Compra, ItemCompra

class ItemCompraSerializer(ModelSerializer):
    produto_nome = SerializerMethodField()
    
    class Meta:
        model = ItemCompra
        fields = [
            'id', 'produto', 'produto_nome', 'quantidade', 
            'preco_unitario', 'subtotal'
        ]
        read_only_fields = ['id', 'subtotal']

    def get_produto_nome(self, obj):
        """Get product name."""
        return obj.produto.nome if obj.produto else None

class CompraSerializer(ModelSerializer):
    fornecedor_nome = SerializerMethodField()
    # Campo do serializer renomeado
    funcionario_nome = SerializerMethodField()
    itens = ItemCompraSerializer(many=True, required=False)
    status_display = SerializerMethodField()
    
    class Meta:
        model = Compra
        fields = [
            'id', 'numero_pedido', 'fornecedor', 'fornecedor_nome',
            'funcionario', 'funcionario_nome', 'data_pedido', 'data_entrega_prevista',
            'data_entrega_real', 'valor_total', 'desconto', 'frete',
            'status', 'status_display', 'observacoes', 'itens'
        ]
        read_only_fields = ['id', 'data_pedido', 'valor_total']

    def get_fornecedor_nome(self, obj):
        """Get supplier name."""
        return obj.fornecedor.nome if obj.fornecedor else None

    def get_funcionario_nome(self, obj):
        """Get user name."""
        return obj.funcionario.nome if obj.funcionario else None

    def get_status_display(self, obj):
        """Get status display name."""
        return obj.get_status_display()

    def create(self, validated_data):
        """Create purchase with items."""
        itens_data = validated_data.pop('itens', [])
        compra = Compra.objects.create(**validated_data)
        
        valor_total = 0
        for item_data in itens_data:
            item = ItemCompra.objects.create(compra=compra, **item_data)
            valor_total += item.subtotal
        
        compra.valor_total = valor_total + compra.frete - compra.desconto
        compra.save()
        return compra

    def update(self, instance, validated_data):
        """Update purchase with items."""
        itens_data = validated_data.pop('itens', [])
        
        # Update purchase fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update items if provided
        if itens_data:
            instance.itens.all().delete()
            valor_total = 0
            for item_data in itens_data:
                item = ItemCompra.objects.create(compra=instance, **item_data)
                valor_total += item.subtotal
            
            instance.valor_total = valor_total + instance.frete - instance.desconto
        
        instance.save()
        return instance