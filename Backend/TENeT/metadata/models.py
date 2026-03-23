from django.db import models

class MetaData(models.Model):
    Lastupdated = models.CharField()
    def save(self, *args, **kwargs):
            self.pk = 1 
            super().save(*args, **kwargs)
# Create your models here.
