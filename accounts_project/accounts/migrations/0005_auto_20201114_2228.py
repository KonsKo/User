# Generated by Django 3.1.2 on 2020-11-14 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20201114_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='date_finished',
            field=models.DateTimeField(blank=True),
        ),
    ]
