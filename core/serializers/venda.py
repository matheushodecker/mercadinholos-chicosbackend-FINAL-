from rest_framework.serializers import ModelSerializer, SerializerMethodField 
from core.models import Venda, ItemVenda 
 
class ItemVendaSerializer(ModelSerializer): 
    produto_nome = SerializerMethodField() 
     
    class Meta: 
        model = ItemVenda 
        fields = [ 
            'id', 'produto', 'produto_nome', 'quantidade',  
            'preco_unitario', 'subtotal' 
        ] 
        read_only_fields = ['id', 'subtotal'] 

    def get_produto_nome(self, obj): 
        """Get product name.""" 
        return obj.produto.nome if obj.produto else None 

class VendaSerializer(ModelSerializer): 
    itens = ItemVendaSerializer(many=True, required=False) 
    funcionario_nome = SerializerMethodField() 
    status_display = SerializerMethodField() 
     
    class Meta: 
        model = Venda 
        fields = [ 
            'id', 'funcionario', 'funcionario_nome', 'data_venda', 'total', 
            'desconto', 'status', 'status_display', 'observacoes', 'itens' 
        ] 
        read_only_fields = ['id', 'data_venda', 'total'] 

    def get_funcionario_nome(self, obj): 
        """Get user name.""" 
        return obj.funcionario.nome if obj.funcionario else None 

    def get_status_display(self, obj): 
        """Get status display name.""" 
        return obj.get_status_display() 

    def create(self, validated_data): 
        """Create sale with items.""" 
        itens_data = validated_data.pop('itens', []) 
        venda = Venda.objects.create(**validated_data) 
         
        total = 0 
        for item_data in itens_data: 
            item = ItemVenda.objects.create(venda=venda, **item_data) 
            total += item.subtotal 
         
        venda.total = total - venda.desconto 
        venda.save() 
        return venda 

    def update(self, instance, validated_data): 
        """Update sale with items.""" 
        itens_data = validated_data.pop('itens', []) 
         
        # Update sale fields 
        for attr, value in validated_data.items(): 
            setattr(instance, attr, value) 
         
        # Update items if provided 
        if itens_data: 
            instance.itens.all().delete() 
            total = 0 
            for item_data in itens_data: 
                item = ItemVenda.objects.create(venda=instance, **item_data) 
                total += item.subtotal 
             
            instance.total = total - instance.desconto 
         
        instance.save() 
        return instance