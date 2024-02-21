from django.db import models

class Booking_service(models.Model):
    booking = models.ForeignKey('booking.Booking', on_delete=models.DO_NOTHING)
    service = models.ForeignKey('service.Service', on_delete=models.DO_NOTHING)
    price = models.IntegerField()
    

    def __str__(self):
        return str(self.price)
