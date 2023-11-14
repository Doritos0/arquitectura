from django.db import models

# Create your models here.

class Usuario (models.Model):
    user = models.CharField(primary_key = True, max_length=20)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.user