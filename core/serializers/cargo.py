from rest_framework.serializers import ModelSerializer
from core.models import Cargo

class CargoSerializer(ModelSerializer):
    class Meta:
        model = Cargo
        fields = [
            'id', 'nome', 'descricao', 'salario_base', 
            'comissao_percentual', 'ativo', 'data_criacao'
        ]
        read_only_fields = ['id', 'data_criacao']