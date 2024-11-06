from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Servidor(AbstractBaseUser):
    matricula = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    FUNCOES = [('p', 'Professor'), ('d', 'Direção'), ('c', 'Cordenação')]
    funcao = models.CharField(max_length=1, choices=FUNCOES)
    ativo = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)
    ult_acesso = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'matricula'
    REQUIRED_FIELDS = ['email', 'senha']

    class Meta:
        verbose_name = 'Servidor'
        verbose_name_plural = 'Servidores'

    def __str__(self):
        funcao_nome = dict(self.FUNCOES).get(self.funcao)
        return f"{funcao_nome} - {self.nome}"



class Horario(models.Model):
    numero_aula = models.PositiveBigIntegerField(unique=True)
    horario = models.TimeField()

class Espaco(models.Model):
    nome = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Reserva(models.Model):
    matricula = models.ForeignKey(Servidor, on_delete=models.CASCADE)
    espaco = models.ForeignKey(Espaco, on_delete=models.CASCADE)
    data = models.DateField()
    motivo = models.TextField(null=True, blank=True)
    turma = models.CharField(max_length=50, null=True, blank=True)
    data_hora_reserva = models.DateTimeField(auto_now_add=True)

class ReservarHorario(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    numero_aula = models.ForeignKey(Horario, on_delete=models.CASCADE)