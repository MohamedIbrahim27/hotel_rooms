# Generated by Django 4.2 on 2023-05-11 06:09

from django.db import migrations, models
import property.models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0006_property_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=property.models.place_image_upload),
        ),
    ]
