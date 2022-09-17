from django.db import models

class DemoImage(models.Model):
    # MEDIA_ROOT 配下の images フォルダを参照
    image = models.ImageField(upload_to='images/')