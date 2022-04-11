from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from django_resized import ResizedImageField


class Album(models.Model):

    TITLE_MAX_LENGTH = 60

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
    )

    thumbnail = models.ImageField(
        upload_to='thumbnails',
        default='default_thumbnail.jpg',
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home page')

    class Meta:
        ordering = ['-id']


class Picture(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    photo = models.ImageField(
        upload_to='album_pictures',
    )

    def get_absolute_url(self):
        return reverse('detail album', kwargs={'pk': self.album.pk})

    class Meta:
        ordering = ['-id']

