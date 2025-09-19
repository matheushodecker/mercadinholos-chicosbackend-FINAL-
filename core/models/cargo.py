from django.db import models
from django.utils import timezone

class Cargo(models.Model):
    """
    Modelo para armazenar os cargos dos funcionários.
    """
    nome = models.CharField(max_length=100, unique=True, help_text="Nome do cargo.")
    descricao = models.TextField(blank=True, help_text="Descrição do cargo.")
    salario_base = models.DecimalField(max_digits=10, decimal_places=2, help_text="Salário base do cargo.")
    comissao_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Percentual de comissão.")
    ativo = models.BooleanField(default=True, help_text="Cargo ativo.")
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        ordering = ['nome']
