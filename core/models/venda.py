from django.db import models
from django.utils import timezone
from .funcionario import Funcionario 
from .produto import Produto

class Venda(models.Model):
    """
    Modelo para armazenar os dados das vendas.
    """
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]

    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, help_text="Funcionário que realizou a venda.")
    data_venda = models.DateTimeField(default=timezone.now, help_text="Data e hora da venda.")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Valor total da venda.")
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Desconto aplicado.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', help_text="Status da venda.")
    observacoes = models.TextField(blank=True, help_text="Observações sobre a venda.")

    def __str__(self):
        return f'Venda #{self.id} - {self.data_venda.strftime("%d/%m/%Y")}'

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
        ordering = ['-data_venda']

class ItemVenda(models.Model):
    """
    Modelo para armazenar os itens de cada venda.
    """
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE, help_text="Venda relacionada.")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, help_text="Produto vendido.")
    quantidade = models.IntegerField(help_text="Quantidade vendida.")
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, help_text="Preço unitário no momento da venda.")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, help_text="Subtotal do item.")

    def save(self, *args, **kwargs):
        """Calcula o subtotal automaticamente."""
        self.subtotal = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.produto.nome} - Qtd: {self.quantidade}'

    class Meta:
        verbose_name = "Item de Venda"
        verbose_name_plural = "Itens de Venda"