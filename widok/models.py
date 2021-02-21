from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

from django.dispatch import receiver
import os
from django.db.models.signals import post_delete,pre_save,post_save

from django.contrib.auth.models import User
# Create your models here.
from PIL import Image, ImageOps


class Obrazek(models.Model):
    obrazek_path = models.CharField(max_length=200,null=True,default=None)
    obrazek_file = models.ImageField(upload_to='img_file',null=True,default=None)

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
        if not self.oceny_set.filter(autor=user).count():
            return 0
        return self.oceny_set.get(autor=user).ocena









@receiver(post_delete, sender=Obrazek)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.obrazek_file:
        os.remove(instance.obrazek_file.path)


@receiver(pre_save, sender=Obrazek)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Obrazek.objects.get(pk=instance.pk).obrazek_file
    except Obrazek.DoesNotExist:
        return False

    new_file = instance.obrazek_file
    if not old_file == new_file:
        os.remove(old_file.path)




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

