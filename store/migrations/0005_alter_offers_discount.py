# Generated by Django 4.1.4 on 2023-02-16 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_remove_offers_dicount_offers_discount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offers',
            name='discount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
