from django.db import models
from django.utils import timezone

class Cliente(models.Model):
    """
    Modelo para armazenar os dados dos clientes.
    """
    TIPO_PESSOA_CHOICES = [
        ('F', 'Pessoa Física'),
        ('J', 'Pessoa Jurídica'),
    ]

    nome = models.CharField(max_length=255, help_text="Nome do cliente.")
    tipo_pessoa = models.CharField(max_length=1, choices=TIPO_PESSOA_CHOICES, default='F', help_text="Tipo de pessoa.")
    cpf_cnpj = models.CharField(max_length=18, unique=True, help_text="CPF ou CNPJ do cliente.")
    rg_ie = models.CharField(max_length=20, blank=True, null=True, help_text="RG ou Inscrição Estadual.")
    
    # Endereço
    endereco = models.CharField(max_length=255, blank=True, help_text="Endereço do cliente.")
    bairro = models.CharField(max_length=100, blank=True, help_text="Bairro do cliente.")
    cidade = models.CharField(max_length=100, blank=True, help_text="Cidade do cliente.")
    estado = models.CharField(max_length=2, blank=True, help_text="Estado do cliente.")
    cep = models.CharField(max_length=9, blank=True, help_text="CEP do cliente.")
    
    # Contato
    telefone = models.CharField(max_length=20, blank=True, help_text="Telefone do cliente.")
    celular = models.CharField(max_length=20, blank=True, help_text="Celular do cliente.")
    email = models.EmailField(max_length=255, blank=True, help_text="Email do cliente.")
    
    # Dados adicionais
    data_nascimento = models.DateField(blank=True, null=True, help_text="Data de nascimento.")
    limite_credito = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Limite de crédito.")
    ativo = models.BooleanField(default=True, help_text="Cliente ativo.")
    data_cadastro = models.DateTimeField(default=timezone.now)
    observacoes = models.TextField(blank=True, help_text="Observações sobre o cliente.")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome']