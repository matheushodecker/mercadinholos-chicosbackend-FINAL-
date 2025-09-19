from rest_framework.serializers import ModelSerializer, SerializerMethodField
from core.models import RelatorioVenda, RelatorioEstoque
from django.utils import timezone  # Adicione esta linha

class RelatorioVendaSerializer(ModelSerializer):
    funcionario_gerador_nome = SerializerMethodField()
    
    class Meta:
        model = RelatorioVenda
        fields = [
            'id', 'nome', 'data_inicio', 'data_fim',
            'total_vendas', 'quantidade_vendas', 'ticket_medio', 
            'funcionario_gerador', 'funcionario_gerador_nome', 'data_geracao', 
            'observacoes'
        ]
        read_only_fields = [
            'id', 'data_geracao', 'total_vendas', 'quantidade_vendas', 
            'ticket_medio'
        ]

    def get_funcionario_gerador_nome(self, obj):
        return obj.funcionario_gerador.nome if obj.funcionario_gerador else None

class RelatorioEstoqueSerializer(ModelSerializer):
    funcionario_gerador_nome = SerializerMethodField()
    
    class Meta:
        model = RelatorioEstoque
        fields = [
            'id', 'nome', 'total_produtos', 'produtos_estoque_baixo', 
            'valor_total_estoque', 'funcionario_gerador', 'funcionario_gerador_nome', 
            'data_geracao', 'observacoes'
        ]
        read_only_fields = [
            'id', 'data_geracao', 'total_produtos', 'produtos_estoque_baixo', 
            'valor_total_estoque'
        ]

    def get_funcionario_gerador_nome(self, obj):
        return obj.funcionario_gerador.nome if obj.funcionario_gerador else None

    def create(self, validated_data):
        total_produtos = validated_data.get('total_produtos')
        produtos_estoque_baixo = validated_data.get('produtos_estoque_baixo')
        valor_total_estoque = validated_data.get('valor_total_estoque')

        relatorio = RelatorioEstoque.objects.create(
            nome=validated_data.get('nome'),
            observacoes=validated_data.get('observacoes', ''),
            funcionario_gerador=validated_data.get('funcionario_gerador'),
            total_produtos=total_produtos,
            produtos_estoque_baixo=produtos_estoque_baixo,
            valor_total_estoque=valor_total_estoque,
            data_geracao=timezone.now()
        )
        return relatorio