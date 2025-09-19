from django.db import models
from django.utils import timezone
from .cargo import Cargo

class Funcionario(models.Model):
    """
    Modelo para armazenar os dados dos funcionários.
    """
    ESTADO_CIVIL_CHOICES = [
        ('S', 'Solteiro'),
        ('C', 'Casado'),
        ('D', 'Divorciado'),
        ('V', 'Viúvo'),
    ]

    nome = models.CharField(max_length=255, help_text="Nome completo do funcionário.")
    cpf = models.CharField(max_length=14, unique=True, help_text="CPF do funcionário.")
    rg = models.CharField(max_length=20, help_text="RG do funcionário.")
    data_nascimento = models.DateField(help_text="Data de nascimento.")
    estado_civil = models.CharField(max_length=1, choices=ESTADO_CIVIL_CHOICES, help_text="Estado civil.")
    
    # Endereço
    endereco = models.CharField(max_length=255, help_text="Endereço do funcionário.")
    bairro = models.CharField(max_length=100, help_text="Bairro do funcionário.")
    cidade = models.CharField(max_length=100, help_text="Cidade do funcionário.")
    estado = models.CharField(max_length=2, help_text="Estado do funcionário.")
    cep = models.CharField(max_length=9, help_text="CEP do funcionário.")
    
    # Contato
    telefone = models.CharField(max_length=20, blank=True, help_text="Telefone do funcionário.")
    celular = models.CharField(max_length=20, help_text="Celular do funcionário.")
    email = models.EmailField(max_length=255, help_text="Email do funcionário.")
    
    # Dados profissionais
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, help_text="Cargo do funcionário.")
    salario = models.DecimalField(max_digits=10, decimal_places=2, help_text="Salário atual.")
    data_admissao = models.DateField(help_text="Data de admissão.")
    data_demissao = models.DateField(blank=True, null=True, help_text="Data de demissão.")
    ativo = models.BooleanField(default=True, help_text="Funcionário ativo.")
    observacoes = models.TextField(blank=True, help_text="Observações sobre o funcionário.")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ['nome']
