from django.db import models

# Create your models here.
class IPLog(models.Model):
    adresse_IP = models.CharField(max_length=200)
    request = models.TextField(max_length=1024)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} | {self.adresse_IP}" 