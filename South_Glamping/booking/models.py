from django.db import models

class Booking(models.Model):
    date_booking = models.DateField()
    date_start = models.DateField()
    date_end = models.DateField()
    price = models.IntegerField()
    status = models.CharField(max_length=30, default = 'Reservado')
    customer = models.ForeignKey('customer.Customer', on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.date_booking)