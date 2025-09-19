from django.db import models
from django.utils import timezone
from .produto import Produto

class Promocao(models.Model):
    """
    Modelo para armazenar as promoções.
    """
    TIPO_DESCONTO_CHOICES = [
        ('P', 'Percentual'),
        ('V', 'Valor Fixo'),
    ]

    nome = models.CharField(max_length=255, help_text="Nome da promoção.")
    descricao = models.TextField(blank=True, help_text="Descrição da promoção.")
    tipo_desconto = models.CharField(max_length=1, choices=TIPO_DESCONTO_CHOICES, help_text="Tipo de desconto.")
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor do desconto.")
    data_inicio = models.DateTimeField(help_text="Data de início da promoção.")
    data_fim = models.DateTimeField(help_text="Data de fim da promoção.")
    ativo = models.BooleanField(default=True, help_text="Promoção ativa.")
    data_criacao = models.DateTimeField(default=timezone.now)

    @property
    def promocao_ativa(self):
        agora = timezone.now()
        return self.ativo and self.data_inicio <= agora <= self.data_fim

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Promoção"
        verbose_name_plural = "Promoções"
        ordering = ['-data_criacao']

class ProdutoPromocao(models.Model):
    """
    Modelo para relacionar produtos com promoções.
    """
    promocao = models.ForeignKey(Promocao, related_name='produtos', on_delete=models.CASCADE, help_text="Promoção relacionada.")
    produto = models.ForeignKey(Produto, related_name='promocoes', on_delete=models.CASCADE, help_text="Produto em promoção.")
    preco_promocional = models.DecimalField(max_digits=10, decimal_places=2, help_text="Preço promocional.")

    def __str__(self):
        return f"{self.produto.nome} - {self.promocao.nome}"

    class Meta:
        verbose_name = "Produto em Promoção"
        verbose_name_plural = "Produtos em Promoção"
        unique_together = ['promocao', 'produto']
