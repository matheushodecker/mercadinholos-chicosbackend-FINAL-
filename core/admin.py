"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'passage_id')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            },
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Groups'), {'fields': ('groups',)}),
        (_('User Permissions'), {'fields': ('user_permissions',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'name',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
    )

# Registrar todos os modelos
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Fornecedor)
admin.site.register(models.Categoria)
admin.site.register(models.Produto)
admin.site.register(models.Cliente)
admin.site.register(models.Funcionario)
admin.site.register(models.Cargo)
admin.site.register(models.Estoque)
admin.site.register(models.MovimentacaoEstoque)
admin.site.register(models.Compra)
admin.site.register(models.ItemCompra)
admin.site.register(models.Venda)
admin.site.register(models.ItemVenda)
admin.site.register(models.FormaPagamento)
admin.site.register(models.Pagamento)
admin.site.register(models.Promocao)
admin.site.register(models.ProdutoPromocao)
admin.site.register(models.RelatorioVenda)
admin.site.register(models.RelatorioEstoque)
