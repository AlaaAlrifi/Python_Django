# Generated by Django 3.2.5 on 2022-07-05 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pharmacy', '0003_auto_20220705_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='buy',
            field=models.BooleanField(default=False),
        ),
    ]
