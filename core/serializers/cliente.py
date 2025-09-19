from rest_framework.serializers import ModelSerializer
from core.models import Cliente

class ClienteSerializer(ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'id', 'nome', 'email', 'telefone', 'cpf_cnpj', 'endereco',
            'cidade', 'estado', 'cep', 'data_nascimento',
            'ativo', 'data_cadastro'
        ]
        read_only_fields = ['id', 'data_cadastro']
        extra_kwargs = {
            'cpf_cnpj': {'write_only': True},  # Campo corrigido para cpf_cnpj
            'email': {'required': True},
        }