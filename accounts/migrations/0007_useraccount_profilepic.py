# Generated by Django 4.0.3 on 2022-03-18 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_useraccount_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='profilePic',
            field=models.ImageField(default='accounts/react.jpg', upload_to='accounts'),
        ),
    ]