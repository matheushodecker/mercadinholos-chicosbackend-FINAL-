from rest_framework.viewsets import ModelViewSet

from core.models import Fornecedor
from core.serializers.fornecedor import FornecedorSerializer


class FornecedorViewSet(ModelViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
