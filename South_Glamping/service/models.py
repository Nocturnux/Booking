from django.db import models


class Service(models.Model):
    image = models.ImageField(upload_to='static/service_images', null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    price = models.IntegerField()
    status = models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.name
