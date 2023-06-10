# Generated by Django 4.2 on 2023-06-07 01:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('property', '0010_propertybook_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='property_owner', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
