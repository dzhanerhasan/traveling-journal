# Generated by Django 4.0.3 on 2022-04-10 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_album_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='picture',
            options={'ordering': ['-id']},
        ),
    ]
