from django.db import models

class User(models.Model):
    date_create = models.DateField()
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=25)
    rol = models.CharField(max_length=25, default = 'Cliente')
    status = models.BooleanField(default=True)
    customer = models.ForeignKey('customer.Customer', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.rol
