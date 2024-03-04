from django.db import models

class Payment(models.Model):
    amount = models.IntegerField(default=0)
    date = models.DateField()
    payment_method = models.CharField(max_length=55)
    status = models.CharField(max_length=25)
    booking = models.ForeignKey('booking.Booking', on_delete=models.DO_NOTHING)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.payment_method
