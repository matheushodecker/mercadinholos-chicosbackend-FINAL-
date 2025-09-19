from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    """
    Modelo para armazenar as categorias dos produtos.
    """
    nome = models.CharField(max_length=100, help_text="Nome da categoria.")
    descricao = models.TextField(blank=True, help_text="Descrição da categoria.")
    ativo = models.BooleanField(default=True, help_text="Indica se a categoria está ativa.")
    data_criacao = models.DateTimeField(default=timezone.now, help_text="Data de criação da categoria.")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']
