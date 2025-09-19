# Arquivo: pagamentos.py

from django.db import models
from django.utils import timezone
from .venda import Venda

class FormaPagamento(models.Model):
    # ... código do modelo FormaPagamento ...
    nome = models.CharField(max_length=100, unique=True, help_text="Nome da forma de pagamento.")
    descricao = models.TextField(blank=True, help_text="Descrição da forma de pagamento.")
    taxa_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Taxa percentual.")
    taxa_fixa = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Taxa fixa.")
    prazo_recebimento = models.IntegerField(default=0, help_text="Prazo para recebimento em dias.")
    ativo = models.BooleanField(default=True, help_text="Forma de pagamento ativa.")
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Forma de Pagamento"
        verbose_name_plural = "Formas de Pagamento"
        ordering = ['nome']

class Pagamento(models.Model):
    # ... código do modelo Pagamento ...
    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('R', 'Recebido'),
        ('C', 'Cancelado'),
    ]

    venda = models.ForeignKey(Venda, related_name='pagamentos', on_delete=models.CASCADE, help_text="Venda relacionada.")
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT, help_text="Forma de pagamento.")
    valor = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor do pagamento.")
    data_vencimento = models.DateField(help_text="Data de vencimento.")
    data_recebimento = models.DateField(blank=True, null=True, help_text="Data de recebimento.")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P', help_text="Status do pagamento.")
    observacoes = models.TextField(blank=True, help_text="Observações do pagamento.")

    def __str__(self):
        # Mude esta linha para usar o ID da venda
        return f"Pagamento para Venda #{self.venda.id} - {self.forma_pagamento.nome}"

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        ordering = ['-data_vencimento']