from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save, post_save
import os
from .models import Obrazek, Kometarz, Oceny
from django.core.cache import cache


@receiver(post_delete, sender=Obrazek)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.obrazek_file:
        os.remove(instance.obrazek_file.path)
    cache.delete('obrazy')


@receiver(post_save, sender=Obrazek)
@receiver(post_save, sender=Oceny)
@receiver(post_save, sender=Kometarz)
def clear_cache(sender, **kwargs):
    cache.clear()

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
