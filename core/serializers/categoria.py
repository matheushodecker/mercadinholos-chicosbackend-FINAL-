from rest_framework.serializers import ModelSerializer
from core.models import Categoria

class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id', 'nome', 'descricao', 'ativo', 
            'data_criacao'  # 'data_atualizacao' was removed
        ]
        read_only_fields = ['id', 'data_criacao']  # 'data_atualizacao' was removed