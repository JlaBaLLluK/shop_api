from django.core.exceptions import ValidationError


def validate_username(username):
    if ' ' in username:
        raise ValidationError("Username can't contain spaces!")
