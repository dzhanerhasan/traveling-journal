from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class CheckList(models.Model):

    TITLE_MAX_LENGTH = 150

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('checklist')

    class Meta:
        ordering = ['-id']


class ListItems(models.Model):

    CONTENT_MAX_LENGTH = 200

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    checklist = models.ForeignKey(
        CheckList,
        on_delete=models.CASCADE,
    )

    content = models.CharField(
        max_length=CONTENT_MAX_LENGTH,
        null=False,
        blank=False,
    )

    completed = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-id']