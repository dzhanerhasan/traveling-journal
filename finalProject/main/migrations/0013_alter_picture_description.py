# Generated by Django 4.0.3 on 2022-04-11 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_album_thumbnail_alter_picture_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='description',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
