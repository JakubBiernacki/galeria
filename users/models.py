from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageOps



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_img')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if (img.height >300 or img.width >300) and self.image.url != '/media/default.jpg':

            pil = ImageOps.exif_transpose(img)
            w, h = pil.size

            output_size = (300,300)

            img.thumbnail(output_size)

            if h>w:
                img = img.rotate(270)
                m_w, m_h = img.size
                to_crop = (m_w - m_h) / 2

                left = to_crop
                top = 0
                right = m_w - to_crop
                bottom = m_h
                img = img.crop((left, top, right, bottom))

            img.save(self.image.path)
