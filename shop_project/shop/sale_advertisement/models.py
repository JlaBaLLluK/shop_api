from django.db import models

from sale_advertisement.validators import price_validator
from user.models import AuthUser


class SaleAdvertisement(models.Model):
    advertisement_title = models.CharField(max_length=150, blank=False)
    advertisement_description = models.TextField(blank=False)
    advertisement_location = models.CharField(max_length=150, blank=False)
    publish_date = models.DateTimeField(auto_now=True)
    advertisement_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False,
                                              validators=[price_validator])
    advertisement_author = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='advertisements')
    is_new = models.BooleanField(blank=False)
    views_amount = models.PositiveIntegerField(default=0)
    users_checked_advertisement = models.ManyToManyField(AuthUser, blank=True, related_name='checked_advertisements',
                                                         default=None, through='AdvertisementsUsers')

    class Meta:
        db_table = 'Advertisements'

    def __str__(self):
        return self.advertisement_title


class AdvertisementsUsers(models.Model):
    advertisement = models.ForeignKey(SaleAdvertisement, on_delete=models.CASCADE)
    user_checked_advertisements = models.ForeignKey(AuthUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'AdvertisementsUsers'
