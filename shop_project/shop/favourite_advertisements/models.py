from django.db import models
from django.contrib.postgres.fields import ArrayField

from sale_advertisement.models import SaleAdvertisement
from user.models import AuthUser


class FavouriteAdvertisements(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    advertisements = models.ManyToManyField(SaleAdvertisement, default=0)
    advertisements_amount = models.PositiveIntegerField(default=0)
    adding_date = ArrayField(models.DateTimeField())

    class Meta:
        db_table = "FavouriteAdvertisements"

    def __str__(self):
        return str(self.adding_date)
