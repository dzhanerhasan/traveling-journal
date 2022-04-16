from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    MALE = 'Male'
    FEMALE = 'Female'
    DO_NOT_SHOW = 'Do not show'

    BIO_MAX_LENGTH = 200

    GENDERS = [(x, x) for x in (MALE, FEMALE, DO_NOT_SHOW)]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    biography = models.TextField(
        null=True,
        blank=True,
        default='No biography yet',
        max_length= BIO_MAX_LENGTH,
    )

    gender = models.CharField(
        max_length=max(len(x) for x, _ in GENDERS),
        choices=GENDERS,
        null=True,
        blank=True,
        default=DO_NOT_SHOW,
    )

    picture = models.ImageField(
        default='default.jpg',
        upload_to='profile_picture',
    )

    def __str__(self):
        return f'{self.user.username}'
