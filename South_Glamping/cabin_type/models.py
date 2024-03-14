from django.db import models


class Cabin_type(models.Model):
    image = models.ImageField(upload_to='static/cabin_type_images', null=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=300, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
