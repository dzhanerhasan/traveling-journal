# Generated by Django 4.0.3 on 2022-04-14 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0007_remove_listitems_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='listitems',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
