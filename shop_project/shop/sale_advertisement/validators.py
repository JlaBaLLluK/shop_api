from rest_framework.exceptions import ValidationError


def price_validator(price):
    if price < 0:
        raise ValidationError('Price must be positive!')