from django.db import models
from sale_advertisement.models import SaleAdvertisement
from user.models import AuthUser


class FavouriteAdvertisements(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    advertisement = models.ForeignKey(SaleAdvertisement, on_delete=models.CASCADE)
    adding_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "FavouriteAdvertisements"

    def __str__(self):
        return str(self.adding_date)
