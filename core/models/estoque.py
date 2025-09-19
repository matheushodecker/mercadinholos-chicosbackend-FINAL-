from django.db import models
from django.utils import timezone
from .produto import Produto
# Importação corrigida para o modelo Funcionario
from .funcionario import Funcionario

class Estoque(models.Model):
    """
    Modelo para controle de estoque dos produtos.
    """
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE, help_text="Produto relacionado.")
    quantidade_atual = models.IntegerField(default=0, help_text="Quantidade atual em estoque.")
    quantidade_minima = models.IntegerField(default=5, help_text="Quantidade mínima em estoque.")
    quantidade_maxima = models.IntegerField(default=1000, help_text="Quantidade máxima em estoque.")
    localizacao = models.CharField(max_length=100, blank=True, help_text="Localização no estoque.")
    data_ultima_movimentacao = models.DateTimeField(auto_now=True)

    @property
    def estoque_baixo(self):
        return self.quantidade_atual <= self.quantidade_minima

    @property
    def estoque_alto(self):
        return self.quantidade_atual >= self.quantidade_maxima

    def __str__(self):
        return f"{self.produto.nome} - Qtd: {self.quantidade_atual}"

    class Meta:
        verbose_name = "Estoque"
        verbose_name_plural = "Estoques"

class MovimentacaoEstoque(models.Model):
    """
    Modelo para registrar movimentações de estoque.
    """
    TIPO_MOVIMENTACAO_CHOICES = [
        ('E', 'Entrada'),
        ('S', 'Saída'),
        ('A', 'Ajuste'),
        ('T', 'Transferência'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, help_text="Produto movimentado.")
    tipo_movimentacao = models.CharField(max_length=1, choices=TIPO_MOVIMENTACAO_CHOICES, help_text="Tipo de movimentação.")
    quantidade = models.IntegerField(help_text="Quantidade movimentada.")
    quantidade_anterior = models.IntegerField(help_text="Quantidade anterior.")
    quantidade_atual = models.IntegerField(help_text="Quantidade atual após movimentação.")
    motivo = models.CharField(max_length=255, help_text="Motivo da movimentação.")
    # Campo 'usuario' renomeado para 'funcionario'
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT, help_text="Funcionário responsável.")
    data_movimentacao = models.DateTimeField(default=timezone.now)
    observacoes = models.TextField(blank=True, help_text="Observações da movimentação.")

    def __str__(self):
        return f"{self.produto.nome} - {self.get_tipo_movimentacao_display()} - {self.quantidade}"

    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-data_movimentacao']