# Generated by Django 4.0.3 on 2022-03-18 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_useraccount_profilepic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='profilePic',
            field=models.FileField(default='accounts/react.jpg', upload_to='accounts'),
        ),
    ]