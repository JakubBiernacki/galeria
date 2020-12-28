from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

from django.contrib.auth.models import User
# Create your models here.



class Obrazek(models.Model):
    obrazek_path = models.CharField(max_length=200)
    tytul = models.CharField(max_length=200)
    data_publikacji = models.DateTimeField(default=timezone.now)
    autor = models.ForeignKey(User,on_delete= models.CASCADE)

    def __str__(self):
        return self.tytul
    def oceny_count(self):
        return self.oceny_set.all().count()

    def srednia_ocen(self):
        return round(sum([int(x.ocena) for x in self.oceny_set.all()])/ self.oceny_count(), 1 ) if self.oceny_count()!=0 else 0

    def czy_ocenil(self,user_id):
        user = User.objects.get(id=user_id)
        return self.oceny_set.filter(autor=user).count()




class Kometarz(models.Model):
    obrazek = models.ForeignKey(Obrazek, on_delete=models.CASCADE)
    autor = models.ForeignKey(User,on_delete= models.CASCADE)
    tresc = models.TextField(max_length=320)
    data_publikacji = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.tresc}_do obrazka_{self.obrazek.id}"


class Oceny(models.Model):
    obrazek = models.ForeignKey(Obrazek, on_delete=models.CASCADE)
    ocena = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(0)])
    autor = models.ForeignKey(User,on_delete= models.CASCADE)
    def __str__(self):
        return f"{self.autor}_ocena: {self.ocena}_obrazka: {self.obrazek.tytul}"

