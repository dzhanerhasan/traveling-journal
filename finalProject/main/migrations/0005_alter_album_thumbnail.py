# Generated by Django 4.0.3 on 2022-04-05 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_album_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='thumbnail',
            field=models.ImageField(default='default_thumbnail', upload_to='thumbnails'),
        ),
    ]
