from rest_framework.serializers import ModelSerializer

from core.models import Fornecedor


class FornecedorSerializer(ModelSerializer):
    class Meta: 
        model = Fornecedor
        fields = '__all__'
