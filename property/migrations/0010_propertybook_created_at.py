# Generated by Django 4.2 on 2023-06-07 00:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0009_category_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertybook',
            name='Created_At',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Created At'),
        ),
    ]
