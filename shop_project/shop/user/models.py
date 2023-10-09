from django.contrib.auth.models import AbstractUser


class AuthUser(AbstractUser):
    class Meta:
        db_table = 'Users'
