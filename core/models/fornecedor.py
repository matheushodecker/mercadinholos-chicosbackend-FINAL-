from encodings.punycode import T
from django.db import models
from django.utils import timezone

class Fornecedor(models.Model):
    """
    Modelo para armazenar os dados dos fornecedores.
    """
    TIPO_PESSOA_CHOICES = [
        ('F', 'Pessoa Física'),
        ('J', 'Pessoa Jurídica'),
    ]

    nome = models.CharField(max_length=255,blank=True, null=True, help_text="Nome comercial do fornecedor.")
    razao_social = models.CharField(max_length=255, blank=True, null=True, help_text="Razão social.")
    tipo_pessoa = models.CharField(max_length=1, choices=TIPO_PESSOA_CHOICES, default='J', help_text="Tipo de pessoa.")
    cnpj_cpf = models.CharField(max_length=18, unique=True, blank=True, help_text="CNPJ ou CPF.")
    inscricao_estadual = models.CharField(max_length=20, blank=True, null=True, help_text="Inscrição Estadual.")
    
    # Endereço
    endereco = models.CharField(max_length=255, blank=True, help_text="Endereço completo.")
    bairro = models.CharField(max_length=100, blank=True, help_text="Bairro.")
    cidade = models.CharField(max_length=100, blank=True, help_text="Cidade.")
    estado = models.CharField(max_length=2, blank=True, help_text="Sigla do estado (SC).")
    cep = models.CharField(max_length=9, blank=True, help_text="CEP no formato XXXXX-XXX.")
    
    # Contato
    telefone = models.CharField(max_length=20, blank=True, help_text="Telefone principal.")
    celular = models.CharField(max_length=20, blank=True, help_text="Celular.")
    email = models.EmailField(max_length=255, blank=True, help_text="Email principal.")
    site = models.URLField(blank=True, help_text="Site da empresa.")
    nome_contato = models.CharField(max_length=100, blank=True, help_text="Nome do contato responsável.")
    
    # Dados comerciais
    prazo_pagamento = models.IntegerField(default=30, help_text="Prazo de pagamento em dias.")
    condicoes_pagamento = models.TextField(blank=True, help_text="Condições de pagamento.")
    limite_credito = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Limite de crédito.")
    
    # Controle
    ativo = models.BooleanField(default=True, help_text="Fornecedor ativo.")
    data_cadastro = models.DateTimeField(default=timezone.now, help_text="Data de cadastro.")
    observacoes = models.TextField(blank=True, help_text="Observações gerais.")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['nome']
