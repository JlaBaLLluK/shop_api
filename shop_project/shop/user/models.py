from django.contrib.auth.models import AbstractUser
from django.db import models

from user.validators import *


class AuthUser(AbstractUser):
    username = models.CharField(max_length=255, blank=False, unique=True, validators=[space_validator])
    email = models.EmailField(max_length=255, blank=False, unique=True)
    first_name = models.CharField(max_length=255, blank=True, unique=False, validators=[space_validator,
                                                                                        non_letters_validator])
    last_name = models.CharField(max_length=255, blank=True, unique=False, validators=[space_validator,
                                                                                       non_letters_validator])

    class Meta:
        db_table = 'Users'
