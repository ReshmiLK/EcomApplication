# Generated by Django 4.1.4 on 2023-02-17 07:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_offers_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='expected_deliverydate',
            field=models.DateField(default=datetime.date(2023, 2, 22)),
        ),
    ]
