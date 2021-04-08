from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
import statistics


class Obrazek(models.Model):
    obrazek_path = models.CharField(max_length=200, null=True, default=None)
    obrazek_file = models.ImageField(upload_to='img_file', null=True, default=None)

    tytul = models.CharField(max_length=200)
    data_publikacji = models.DateTimeField(default=timezone.now)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.tytul

    def srednia_ocen(self):
        if oceny := self.oceny_set.all():
            avg = sum([x.ocena for x in oceny]) / oceny.count()
            return round(avg, 1)
        return 0


class Kometarz(models.Model):
    obrazek = models.ForeignKey(Obrazek, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    tresc = models.TextField(max_length=320)
    data_publikacji = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.tresc}_do obrazka_{self.obrazek.id}"


class Oceny(models.Model):
    obrazek = models.ForeignKey(Obrazek, on_delete=models.CASCADE)
    ocena = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.autor}_ocena: {self.ocena}_obrazka: {self.obrazek.tytul}"
