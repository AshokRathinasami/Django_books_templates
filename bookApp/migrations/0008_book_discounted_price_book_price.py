# Generated by Django 5.1 on 2024-09-21 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookApp', '0007_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='discounted_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]