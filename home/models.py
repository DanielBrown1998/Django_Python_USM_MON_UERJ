from django.db import models
from django.contrib.auth.models import User

class Matriculas(models.Model):
    
    class Meta:
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'

    matricula = models.CharField(max_length=12, unique=True)
    status = models.BooleanField(default=False)


# Create your models here.
class DataUser(models.Model):

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    monitorias_marcadas = models.IntegerField(default=0)        
    monitorias_presentes = models.IntegerField(default=0)
    monitorias_ausentes = models.IntegerField(default=0)
    monitorias_canceladas = models.IntegerField(default=0)
    phone = models.CharField(max_length=11, null=True)
 
    def __str__(self):
        return self.owner.first_name + self.owner.last_name


class Monitorias(models.Model):

    estados = [
        ('AUSENTE', 'Ausente'),
        ('PRESENTE', 'Presente'),
        ('CANCELADA', 'Cancelada')
    ]

    date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        default='MARCADA', choices=estados, max_length=15
    )
 
    class Meta:
        verbose_name_plural = "Monitorias"
        unique_together = ('date', 'owner'),

    def __str__(self):
        return self.date.strftime("%d/%m/%Y") + " - " + self.owner.first_name

class Days(models.Model):

    class Meta:
        verbose_name = "Dia"
        verbose_name_plural = "Dias"

    day = models.CharField(max_length=20)

    def __str__(self):
        return self.day

class Horas(models.Model):

    class Meta:
        verbose_name = "Hora"
        verbose_name_plural = "Horas"
        unique_together = 'time', 'day'

    time = models.TimeField()
    day = models.ForeignKey(Days, on_delete=models.CASCADE)
