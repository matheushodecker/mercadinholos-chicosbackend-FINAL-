from rest_framework.serializers import ModelSerializer, SerializerMethodField
from core.models import Funcionario

class FuncionarioSerializer(ModelSerializer):
    cargo_nome = SerializerMethodField()
    
    class Meta:
        model = Funcionario
        fields = [
            'id', 'nome', 'email', 'telefone', 'cpf', 'cargo', 'cargo_nome',
            'salario', 'data_admissao', 'data_demissao', 'endereco',
            'ativo' # 'data_criacao' e 'data_atualizacao' foram removidos
        ]
        read_only_fields = ['id'] # 'data_criacao' e 'data_atualizacao' foram removidos
        extra_kwargs = {
            'cpf': {'write_only': True},   # Sensitive data
            'salario': {'write_only': True},   # Sensitive data
        }

    def get_cargo_nome(self, obj):
        """Get position name."""
        return obj.cargo.nome if obj.cargo else None