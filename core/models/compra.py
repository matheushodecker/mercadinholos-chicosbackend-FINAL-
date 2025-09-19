from django.db import models
from django.utils import timezone
from .fornecedor import Fornecedor
from .produto import Produto
# Importação corrigida para o modelo Funcionario
from .funcionario import Funcionario

class Compra(models.Model):
    """
    Modelo para armazenar as compras realizadas.
    """
    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('A', 'Aprovada'),
        ('R', 'Recebida'),
        ('C', 'Cancelada'),
    ]

    numero_pedido = models.CharField(max_length=50, unique=True, help_text="Número do pedido de compra.")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, help_text="Fornecedor da compra.")
    # Campo 'usuario' renomeado para 'funcionario'
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT, help_text="Funcionário responsável pela compra.")
    data_pedido = models.DateTimeField(default=timezone.now, help_text="Data do pedido.")
    data_entrega_prevista = models.DateField(help_text="Data prevista para entrega.")
    data_entrega_real = models.DateField(blank=True, null=True, help_text="Data real de entrega.")
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Valor total da compra.")
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Desconto aplicado.")
    frete = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Valor do frete.")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P', help_text="Status da compra.")
    observacoes = models.TextField(blank=True, help_text="Observações da compra.")

    def __str__(self):
        return f"Compra {self.numero_pedido} - {self.fornecedor.nome}"

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ['-data_pedido']

class ItemCompra(models.Model):
    """
    Modelo para armazenar os itens de cada compra.
    """
    compra = models.ForeignKey(Compra, related_name='itens', on_delete=models.CASCADE, help_text="Compra relacionada.")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, help_text="Produto comprado.")
    quantidade = models.IntegerField(help_text="Quantidade comprada.")
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, help_text="Preço unitário de compra.")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, help_text="Subtotal do item.")

    def save(self, *args, **kwargs):
        self.subtotal = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produto.nome} - Qtd: {self.quantidade}"

    class Meta:
        verbose_name = "Item de Compra"
        verbose_name_plural = "Itens de Compra"