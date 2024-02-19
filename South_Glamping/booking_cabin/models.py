from django.db import models

class Booking_cabin(models.Model):
    cabin = models.ForeignKey('cabin.Cabin', on_delete=models.DO_NOTHING)
    booking = models.ForeignKey('booking.Booking', on_delete=models.DO_NOTHING)
    price = models.IntegerField()

    def __str__(self):
        return str(self.price)
