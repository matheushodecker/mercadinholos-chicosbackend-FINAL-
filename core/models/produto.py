from django.db import models
from django.utils import timezone
from .categoria import Categoria
from .fornecedor import Fornecedor

class Produto(models.Model):
    """
    Modelo para armazenar os dados dos produtos.
    """
    nome = models.CharField(max_length=200, help_text="Nome do produto.")
    descricao = models.TextField(blank=True, help_text="Descrição do produto.")
    codigo_barras = models.CharField(max_length=50, unique=True, help_text="Código de barras único do produto.")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, help_text="Categoria do produto.")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, help_text="Fornecedor do produto.")
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, help_text="Preço de custo do produto.")
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, help_text="Preço de venda do produto.")
    estoque_atual = models.IntegerField(default=0, help_text="Quantidade atual em estoque.")
    estoque_minimo = models.IntegerField(default=5, help_text="Quantidade mínima em estoque.")
    ativo = models.BooleanField(default=True, help_text="Indica se o produto está ativo.")
    data_criacao = models.DateTimeField(default=timezone.now)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    @property
    def margem_lucro(self):
        """Calcula a margem de lucro em percentual."""
        if self.preco_custo > 0:
            return ((self.preco_venda - self.preco_custo) / self.preco_custo) * 100
        return 0

    @property
    def estoque_baixo(self):
        """Verifica se o estoque está baixo."""
        return self.estoque_atual <= self.estoque_minimo

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome']
