# Generated by Django 4.0.3 on 2022-03-19 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_useraccount_profilepic'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='relative_email',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='relative_email_second',
            field=models.CharField(default='', max_length=15),
        ),
    ]
