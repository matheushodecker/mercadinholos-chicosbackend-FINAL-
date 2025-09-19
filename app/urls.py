from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

from core.views import (
    UserViewSet, FornecedorViewSet,
    CategoriaViewSet, ProdutoViewSet, ClienteViewSet,
    FuncionarioViewSet, CargoViewSet, EstoqueViewSet,
    MovimentacaoEstoqueViewSet, CompraViewSet, VendaViewSet,
    FormaPagamentoViewSet, PagamentoViewSet, PromocaoViewSet,
    RelatorioVendaViewSet, RelatorioEstoqueViewSet
)

router = DefaultRouter()

# Rotas principais
router.register(r'usuarios', UserViewSet, basename='usuarios')
router.register(r'fornecedores', FornecedorViewSet, basename='fornecedores')
router.register(r'categorias', CategoriaViewSet, basename='categorias')
router.register(r'produtos', ProdutoViewSet, basename='produtos')
router.register(r'clientes', ClienteViewSet, basename='clientes')
router.register(r'funcionarios', FuncionarioViewSet, basename='funcionarios')
router.register(r'cargos', CargoViewSet, basename='cargos')

# Rotas de estoque
router.register(r'estoques', EstoqueViewSet, basename='estoques')
router.register(r'movimentacoes-estoque', MovimentacaoEstoqueViewSet, basename='movimentacoes-estoque')

# Rotas de compras e vendas
router.register(r'compras', CompraViewSet, basename='compras')
router.register(r'vendas', VendaViewSet, basename='vendas')

# Rotas de pagamento
router.register(r'formas-pagamento', FormaPagamentoViewSet, basename='formas-pagamento')
router.register(r'pagamentos', PagamentoViewSet, basename='pagamentos')

# Rotas de promoções
router.register(r'promocoes', PromocaoViewSet, basename='promocoes')

# Rotas de relatórios
router.register(r'relatorios-vendas', RelatorioVendaViewSet, basename='relatorios-vendas')
router.register(r'relatorios-estoque', RelatorioEstoqueViewSet, basename='relatorios-estoque')

urlpatterns = [
    path('admin/', admin.site.urls),
    # OpenAPI 3
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    # API
    path('api/', include(router.urls)),
]
