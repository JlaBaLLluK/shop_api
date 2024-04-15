from rest_framework.exceptions import ValidationError


def space_validator(value):
    value = value.strip()
    if ' ' in value:
        raise ValidationError("Can't contain spaces!")


def non_letters_validator(value):
    if not value.isalpha():
        raise ValidationError("Can contain only letters!")
