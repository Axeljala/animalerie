from django.db import models
from django.utils import timezone

# Create your models here.
class Equipement(models.Model):
    id_equip = models.CharField(max_length=20, primary_key=True)
    disponibilite = models.CharField(max_length=20)
    photo = models.CharField(max_length=200)

    def __str__(self):
        return self.id_equip


class Animal(models.Model):
    id_animal = models.CharField(max_length=20, primary_key=True)
    etat = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    race = models.CharField(max_length=20)
    photo = models.CharField(max_length=200)
    lieu = models.ForeignKey(Equipement, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.id_animal

    def naissance(self):
        self.date = timezone.now()
        self.save()
