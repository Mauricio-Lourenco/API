from django.db import models

class Voos(models.Model):
    id = models.AutoField(primary_key=True, default=0)
    airline = models.CharField(max_length=3, default='')
    flight = models.IntegerField(default=0)
    airpot_from = models.CharField(max_length=3, default='')
    airpot_to = models.CharField(max_length=3, default='')
    day_of_week = models.CharField(max_length=1, default=0)
    time = models.IntegerField(default=0)
    delay = models.IntegerField(default=0)

    def __str__(self):
        return f'Id: {self.id} | Airline: {self.airline}'


class Resultado_ia(models.Model):
    id = models.AutoField(primary_key=True)
    voos = models.OneToOneField(Voos, on_delete=models.CASCADE)
    resultado = models.CharField(max_length=150)
