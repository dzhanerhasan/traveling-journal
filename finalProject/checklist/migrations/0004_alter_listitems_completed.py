# Generated by Django 4.0.3 on 2022-04-12 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0003_alter_listitems_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listitems',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
