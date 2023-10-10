from django.db import models

from user.models import AuthUser


class SaleAdvertisement(models.Model):
    advertisement_title = models.CharField(max_length=150, blank=False)
    advertisement_description = models.TextField(blank=False)
    advertisement_location = models.CharField(max_length=150, blank=False)
    publish_date = models.DateTimeField(auto_now=True)
    advertisement_price = models.DecimalField(max_digits=10, decimal_places=2)
    CURRENCIES = [
        ('BYN', 'Belorussian rubles'),
        ('RUB', 'Russian rubles'),
        ('USD', 'American dollars'),
        ('EUR', 'Euro')
    ]
    currency = models.CharField(max_length=3, blank=False, choices=CURRENCIES)
    advertisement_author = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    is_new = models.BooleanField(blank=False)
    views_amount = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'Advertisements'
