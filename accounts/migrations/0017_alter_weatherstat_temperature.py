# Generated by Django 4.0.3 on 2022-04-27 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_weatherstat_time_noted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weatherstat',
            name='temperature',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True),
        ),
    ]
